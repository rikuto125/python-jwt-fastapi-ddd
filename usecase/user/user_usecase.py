from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid
from fastapi import Depends

from domain.user.user import User
from domain.user.user_repsotory import UserRepository
from packages.Jwt import create_access_token, oauth2_scheme, verify_token
from packages.password import get_password_hash, verify_password
from usecase.user.user_command_model import UserCreateModel
from usecase.user.user_query_model import UserReadModel


class UserCommandUseCaseUnitOfWork(ABC):
    """UserCommandUseCaseUnitOfWork defines an interface based on Unit of Work pattern."""

    user_repository: UserRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class UserCommandUseCase(ABC):
    """UserCommandUseCase defines a command usecase inteface related User entity."""

    @abstractmethod
    def create_user(self, data: UserCreateModel) -> Optional[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def login_create_token(self, email: str, password: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> Optional[UserReadModel]:
        raise NotImplementedError


class UserCommandUseCaseImpl(UserCommandUseCase):
    """UserCommandUseCaseImpl implements a command usecases related User entity."""

    def __init__(
            self,
            uow: UserCommandUseCaseUnitOfWork,
    ):
        self.uow: UserCommandUseCaseUnitOfWork = uow

    def create_user(self, data: UserCreateModel) -> Optional[UserReadModel]:
        try:
            uuid = shortuuid.uuid()
            data.hashed_password = get_password_hash(data.hashed_password)
            user = User(id=uuid, name=data.name, email=data.email, hashed_password=data.hashed_password)
            existing_user = self.uow.user_repository.find_by_email(user.email)
            if existing_user is not None:
                raise ValueError("User already exists")

            self.uow.user_repository.create(user)
            self.uow.commit()

            created_user = self.uow.user_repository.find_by_id(uuid)

        except:
            self.uow.rollback()
            raise

        return UserReadModel.from_entity(cast(User, created_user))

    def login_create_token(self, email: str, password: str) -> Optional[str]:
        try:
            user = self.uow.user_repository.find_by_email(email)
            if user is None:
                raise ValueError("User not found")
            if not verify_password(password, user.hashed_password):
                raise ValueError("Password is not correct")

            token = create_access_token(data={"sub": user.email})
            return token

        except:
            self.uow.rollback()
            raise

    def get_current_user(
            self,
            token: str = Depends(oauth2_scheme),
    ) -> Optional[UserReadModel]:
        try:
            email = verify_token(token)
            user = self.uow.user_repository.find_by_email(email)
            if user is None:
                raise ValueError("User not found")
            return UserReadModel.from_entity(cast(User, user))

        except:
            self.uow.rollback()
            raise