from typing import cast

from pydantic import BaseModel, Field

from domain.user.user import User


class UserReadModel(BaseModel):
    id: str = Field(example=1)
    name: str = Field(example="John Doe")
    email: str = Field(example="aaa@gmail.com")
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(user: User) -> "UserReadModel":
        return UserReadModel(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=cast(int, user.created_at),
            updated_at=cast(int, user.updated_at),
        )