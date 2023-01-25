import pathlib
import pydantic
import decouple

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()


class BackendBaseSettings(pydantic.BaseSettings):
    # General
    SERVER_HOST: str = decouple.config("BACKEND_SERVER_HOST", cast=str)
    SERVER_PORT: int = decouple.config("BACKEND_SERVER_PORT", cast=int)
    SERVER_WORKERS: int = decouple.config("BACKEND_SERVER_WORKERS", cast=int)
    DEBUG: bool = decouple.config("BACKEND_DEBUG", cast=bool)
    LOGGING_LEVEL: str = decouple.config("BACKEND_LOGGING_LEVEL", cast=str)

    # Middleware
    CORS_HOSTS: list[str] = decouple.config("BACKEND_HOST", cast=list[str])
    CORS_ORIGINS: list[str] = decouple.config("BACKEND_CORS_ORIGIN", cast=list[str])
    CORS_CREDENTIALS: bool = decouple.config("BACKEND_CORS_CREDENTIALS", cast=bool)
    CORS_METHODS: list[str] = decouple.config("BACKEND_CORS_METHODS", cast=list[str])
    CORS_HEADERS: list[str] = decouple.config("BACKEND_CORS_HEADERS", cast=list[str])
    CORS_MAXAGE: int = decouple.config("BACKEND_CORS_MAXAGE", cast=int)

    # Database
    DATABASE_DRIVER: str = decouple.config("DATABASE_DRIVER", cast=str)
    DATABASE_NAME: str = decouple.config("DATABASE_NAME", cast=str)  # db
    DATABASE_HOST: str = decouple.config("DATABASE_HOST", cast=str)  # postgresserver
    DATABASE_PORT: str = decouple.config("DATABASE_PORT", cast=str)  # 5432
    DATABASE_USER: str = decouple.config("DATABASE_USER", cast=str)  # user
    DATABASE_PASSWORD: str = decouple.config("DATABASE_PASSWORD", cast=str)  # password
    DATABASE_URL: str = DATABASE_DRIVER + "://" + DATABASE_USER + ":" + DATABASE_PASSWORD + "@" + DATABASE_HOST + ":" + str(DATABASE_PORT) + "/" + DATABASE_NAME

    # JWT
    JWT_SECRET_KEY: str = decouple.config("JWT_SECRET_KEY", cast=str)
    JWT_ALGORITHM: str = decouple.config("JWT_ALGORITHM", cast=str)
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = decouple.config("JWT_ACCESS_TOKEN_EXPIRE", cast=int)
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = decouple.config("JWT_REFRESH_TOKEN_EXPIRE", cast=int)

    class Config:
        env_file = ROOT_DIR / ".env"
        env_file_encoding = "utf-8"


settings = BackendBaseSettings()

