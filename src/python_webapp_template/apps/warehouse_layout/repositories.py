import json
from abc import ABC, abstractmethod
from collections import defaultdict

from neo4j import AsyncTransaction
from pydantic_core import to_json

from python_webapp_template.apps.warehouse_layout.domain import WarehouseLayout
from python_webapp_template.managers.neo4j_manager import Neo4JManager


class WarehouseLayoutRepository(ABC):
    @abstractmethod
    async def get_warehouse_layout_by_slug(self, slug: str) -> WarehouseLayout:
        pass

    @abstractmethod
    async def upsert_warehouse_layout(self, warehouse_layout: WarehouseLayout):
        pass


class Neo4JWarehouseLayoutRepository(WarehouseLayoutRepository):
    def __init__(self, neo4j_manager: Neo4JManager):
        super().__init__()
        self.neo4j_manager = neo4j_manager

    async def get_warehouse_layout_by_slug(self, slug: str) -> WarehouseLayout:
        pass

    async def upsert_warehouse_layout(self, warehouse_layout: WarehouseLayout):
        async def transaction_function(tx: AsyncTransaction):
            # Delete previous data.
            delete_layout_props = {'slug': warehouse_layout.slug}
            delete_layout_query = """
                MATCH (n {layout_slug: $props.slug})
                DETACH DELETE n
            """
            await tx.run(
                query=delete_layout_query,
                props=json.loads(to_json(delete_layout_props)),
            )

            # Create waypoints.
            create_waypoints_props = [
                {
                    "layout_slug": warehouse_layout.slug,
                    **waypoint.model_dump(),
                }
                for waypoint in warehouse_layout.waypoints
            ]
            create_waypoints_query = """
                UNWIND $props AS prop
                CREATE (n:Waypoint)
                SET n = prop
            """
            await tx.run(
                query=create_waypoints_query,
                props=json.loads(to_json(create_waypoints_props)),
            )

            # Create locations.
            create_locations_props = [
                {
                    "layout_slug": warehouse_layout.slug,
                    **location.model_dump(),
                }
                for location in warehouse_layout.locations
            ]
            create_locations_query = """
                UNWIND $props AS prop
                CREATE (n:Location)
                SET n = prop
            """
            await tx.run(
                query=create_locations_query,
                props=json.loads(to_json(create_locations_props)),
            )

            # Create waypoint to waypoint relationships.
            waypoint_to_edge_map = defaultdict(list)
            for edge in warehouse_layout.waypoint_to_waypoint_edges:
                waypoint_to_edge_map[edge.waypoint_id].append(
                    {
                        "target_id": edge.target_waypoint_id,
                        "properties": edge.model_dump(exclude={"waypoint_id", "target_waypoint_id"}),
                    }
                )

            create_w2w_rels_props = {
                "slug": warehouse_layout.slug,
                "waypoint_ids": list(waypoint_to_edge_map.keys()),
                "edges": dict(waypoint_to_edge_map),
            }
            create_w2w_rels_query = """
                UNWIND $props.waypoint_ids AS wp_id
                UNWIND $props.edges[wp_id] AS relationship
                MATCH (source:Waypoint{layout_slug: $props.slug}),
                      (target:Waypoint{layout_slug: $props.slug})
                WHERE source.id=wp_id AND target.id=relationship.target_id
                CREATE (source)-[r:CONNECTS]->(target)
                SET r = relationship.properties
            """
            await tx.run(
                query=create_w2w_rels_query,
                props=json.loads(to_json(create_w2w_rels_props)),
            )

            # Create waypoint to location relationships.
            waypoint_to_edge_map = defaultdict(list)
            for edge in warehouse_layout.waypoint_to_location_edges:
                waypoint_to_edge_map[edge.waypoint_id].append(
                    {
                        "target_id": edge.target_location_id,
                        "properties": edge.model_dump(exclude={"waypoint_id", "target_location_id"}),
                    }
                )

            create_w2l_rels_props = {
                "slug": warehouse_layout.slug,
                "waypoint_ids": list(waypoint_to_edge_map.keys()),
                "edges": dict(waypoint_to_edge_map),
            }
            create_w2l_rels_query = """
                UNWIND $props.waypoint_ids AS wp_id
                UNWIND $props.edges[wp_id] AS relationship
                MATCH (source:Waypoint{layout_slug: $props.slug}),
                      (target:Location{layout_slug: $props.slug})
                WHERE source.id=wp_id AND target.id=relationship.target_id
                CREATE (source)-[r:ACCESSES]->(target)
                SET r = relationship.properties
            """
            await tx.run(
                query=create_w2l_rels_query,
                props=json.loads(to_json(create_w2l_rels_props)),
            )

        driver = self.neo4j_manager.get_driver()
        async with driver.session() as session:
            await session.execute_write(
                transaction_function=transaction_function,
            )
