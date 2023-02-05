from datetime import datetime
from typing import Union
from sqlalchemy import Column, Integer, String

from domain.user.user import User
from driver.rdb import Base


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
