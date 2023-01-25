from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid

from domain.user.user import User
from domain.user.user_repsotory import UserRepository
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
            user = User(id=uuid, email=data.email, hashed_password=data.hashed_password)
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
