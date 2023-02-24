from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config.settings.base import settings

# dbの設定
DATABASE_DRIVER = settings.DATABASE_DRIVER
USER_NAME = settings.DATABASE_USER
PASSWORD = settings.DATABASE_PASSWORD
HOST = settings.LOCAL_DATABASE_HOST
PORT = settings.DATABASE_PORT
DB_NAME = settings.DATABASE_NAME

# localからdockerに接続する場合は、HOSTをDOCKER_DATABASE_HOSTに変更する

print("DB接続開始")
print(settings.DOCKER_DATABASE_URL)

engine = create_engine(
    settings.DOCKER_DATABASE_URL
    #settings.LOCAL_DATABASE_URL
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()


def create_tables():
    # テーブルを作成する
    Base.metadata.create_all(bind=engine)


"""
BaseとSessionLocal()は、
SQLAlchemyを使用したデータベース操作において、重要な役割を持ちます。
Baseは、SQLAlchemyのdeclarative_base()関数を使用して作成される、
ORM（オブジェクトリレーショナルマッパー）のベースクラスです。
このクラスは、データベースのテーブルとPythonのクラスをマッピングするために使用されます。
SessionLocal()は、SQLAlchemyのsessionmaker()関数を使用して作成される、
セッションクラスです。
このクラスは、データベースへの接続やトランザクション管理、クエリ実行などを行うために使用されます。
BaseとSessionLocal()は、それぞれ異なる役割を持ちますが、
組み合わせることで、ORMを使用したデータベース操作を実現することができます。
Baseを使用して作成したクラスを使用して、データベースのテーブルに対応するPythonのクラスを作成します。
そして、SessionLocal()を使用して作成したセッションを使用して、
そのクラスとデータベースを接続し、データベース操作を行います。
"""
