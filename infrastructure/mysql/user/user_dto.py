from datetime import datetime
from typing import Union
from sqlalchemy import Column, Integer, String

from domain.user.user import User
from driver.rdb import Base
from usecase.user.user_query_model import UserReadModel


def unixTimestamp() -> int:
    # 後で日本時間にする必要がある
    return int(datetime.now().timestamp())


class UserDTO(Base):
    __tablename__ = 'users'
    id: Union[str, Column] = Column(String(255), primary_key=True, index=True)
    name: Union[str, Column] = Column(String(255), nullable=False)
    email: Union[str, Column] = Column(String(255), nullable=False, unique=True)
    hashed_password: Union[str, Column] = Column(String(255), nullable=False)
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            hashed_password=self.hashed_password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> UserReadModel:
        return UserReadModel(
            id=self.id,
            name=self.name,
            email=self.email,
            hashed_password=self.hashed_password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(user: User) -> "UserDTO":
        now = unixTimestamp()
        return UserDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=now,
            updated_at=now,
        )


"""
to_entityメソッドは、
BookDTOオブジェクトをBookエンティティに変換するメソッドです。
Bookエンティティは、ドメインモデルの一部であり、ビジネスルールに従って操作を行います。
to_entityメソッドは、データベースから取得したBookDTOオブジェクトを、ドメインモデルで扱えるBookエンティティに変換するために使用されます。

to_read_modelメソッドは、
BookDTOオブジェクトを読み取り専用のBookReadModelオブジェクトに変換するメソッドです。
BookReadModelは、読み取り専用のデータモデルであり、
データの取得と表示に使用されます。読み取り専用のデータモデルは、ドメインモデルとは異なり、ビジネスルールを持ちません。

from_entityメソッドは、
BookエンティティをBookDTOオブジェクトに変換するメソッドです。
このメソッドは、Bookエンティティを永続化するために使用されるデータベースオブジェクトであるため、
BookDTOクラス内に定義されています。
これにより、BookエンティティをBookDTOオブジェクトに変換し、データベースに保存することができます。
"""
