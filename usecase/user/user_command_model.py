from pydantic import BaseModel, Field, validator


class UserCreateModel(BaseModel):
    """UserCreateModel represents a write model to create a user."""

    name: str = Field(example="John Doe")
    email: str = Field(example="aaaa@gmail.com")
    hashed_password: str = Field(example="hashed_password")
