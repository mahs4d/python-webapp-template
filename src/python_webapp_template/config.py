from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="python_webapp_",
        case_sensitive=False,
    )

    debug: bool = False

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "API Title"
    api_summary: str = "API Summary"
    api_description: str = "API Description"
    api_version: str = "0.1.0"

    neo4j_host: str = "localhost"
    neo4j_port: int = 7687
    neo4j_username: str = "neo4j"
    neo4j_password: str = "password"
    neo4j_database: str = "neo4j"
