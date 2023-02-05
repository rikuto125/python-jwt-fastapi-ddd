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
    CORS_HOSTS:str = decouple.config("BACKEND_HOST", default="", cast=str)
    CORS_ORIGINS:list[str] = decouple.config("BACKEND_CORS_ALLOW_ORIGIN", default="", cast=str).split(",")
    CORS_CREDENTIALS: bool = decouple.config("BACKEND_CORS_CREDENTIALS", cast=bool)
    CORS_METHODS: list[str] = decouple.config("BACKEND_CORS_METHODS", default="", cast=str).split(",")
    CORS_HEADERS: list[str] = decouple.config("BACKEND_CORS_HEADERS", default="", cast=str).split(",")
    CORS_MAXAGE: int = decouple.config("BACKEND_CORS_MAXAGE", cast=int)

    # Database
    DATABASE_DRIVER: str = decouple.config("DATABASE_DRIVER", cast=str)
    DATABASE_NAME: str = decouple.config("DATABASE_NAME", cast=str)  # db
    LOCAL_DATABASE_HOST: str = decouple.config("LOCAL_DATABASE_HOST", cast=str)  # postgresserver
    DOCKER_DATABASE_HOST: str = decouple.config("DOCKER_DATABASE_HOST", cast=str)  # docker-compose.ymlのservice名
    DATABASE_PORT: str = decouple.config("DATABASE_PORT", cast=str)  # 5432
    DATABASE_USER: str = decouple.config("DATABASE_USER", cast=str)  # user
    DATABASE_PASSWORD: str = decouple.config("DATABASE_PASSWORD", cast=str)  # password
    LOCAL_DATABASE_URL: str = DATABASE_DRIVER + "://" + DATABASE_USER + ":" + DATABASE_PASSWORD + "@" + LOCAL_DATABASE_HOST + ":" + DATABASE_PORT + "/" + DATABASE_NAME

    DOCKER_DATABASE_URL: str = DATABASE_DRIVER + "://" + DATABASE_USER + ":" + DATABASE_PASSWORD + "@" + DOCKER_DATABASE_HOST + ":" +DATABASE_PORT + "/" + DATABASE_NAME

    # JWT
    JWT_SECRET_KEY: str = decouple.config("JWT_SECRET_KEY", cast=str)
    JWT_ALGORITHM: str = decouple.config("JWT_ALGORITHM", cast=str)
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = decouple.config("JWT_ACCESS_TOKEN_EXPIRE", cast=int)
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = decouple.config("JWT_REFRESH_TOKEN_EXPIRE", cast=int)

    # Password
    PASSWORD_SALT: str = decouple.config("PASSWORD_SALT", cast=str)
    HASH_ALGORITHM: str = decouple.config("HASH_ALGORITHM", cast=str)

    class Config:
        env_file = ROOT_DIR / ".env"
        env_file_encoding = "utf-8"


settings = BackendBaseSettings()

