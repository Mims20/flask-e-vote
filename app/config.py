from pydantic import BaseSettings


class Configs(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Configs()
