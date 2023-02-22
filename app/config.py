from pydantic import BaseSettings


class Configs(BaseSettings):
    database_username: str = "postgres"
    database_password: str = "0271249352"
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_name: str = "evote"
    secret_key: str = "72bee1348d89e37479c47c5e9677771546723dcc2ec7649b969941ca6fe7298e"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Configs()
