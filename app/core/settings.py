import string

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Celery API"
    admin_email: str
    admin_password: str

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: str


settings = Settings()
