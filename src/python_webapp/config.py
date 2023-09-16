from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="python_webapp_",
        case_sensitive=False,
    )

    debug: bool = False

    system_name: str = "python-webapp-template"
    system_version: str = "0.1.0"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "API Title"
    api_summary: str = "API Summary"
    api_description: str = "API Description"
    api_version: str = "0.1.0"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "user"
    postgres_password: str = "pass"
    postgres_db_name: str = "python_webapp"
