import fastapi
from starlette.middleware.cors import CORSMiddleware

from adapter.controller.http import user
from config.settings.base import settings
from driver.rdb import create_tables


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI()

    @app.on_event("startup")
    async def startup_event():
        create_tables()

    # app.add_middleware(DBSessionMiddleware, db_url=engine)

    # CORSの設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )

    # ルーティングの設定
    app.include_router(router=user.router)

    return app
