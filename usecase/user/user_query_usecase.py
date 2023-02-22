from abc import ABC, abstractmethod
from typing import Optional
from domain.user.user_repsotory import UserRepository
from usecase.user.user_query_model import UserReadModel
from usecase.user.user_query_service import UserQueryService


class UserQueryUseCaseUnitOfWork(ABC):
    """UserQueryUseCaseUnitOfWork defines an interface based on Unit of Work pattern."""

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


class UserQueryUseCase(ABC):
    """UserQueryUseCase defines a command usecase inteface related User entity."""

    @abstractmethod
    def fetch_user_by_id(self, id: str) -> Optional[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_users(self) -> Optional[list[UserReadModel]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_user_by_email(self, email: str) -> Optional[UserReadModel]:
        raise NotImplementedError


class UserQueryUseCaseImpl(UserQueryUseCase):
    """UserQueryUseCaseImpl implements a command usecases related User entity."""

    def __init__(self, user_query_service: UserQueryService):
        self.user_query_service: UserQueryService = user_query_service

    def fetch_user_by_id(self, id: str) -> Optional[UserReadModel]:
        try:
            user = self.user_query_service.find_by_id(id)
            if user is None:
                raise ValueError("User not found")

        except:
            raise ValueError("User not found")

        return user

    def fetch_users(self) -> Optional[list[UserReadModel]]:
        try:
            users = self.user_query_service.find_all()

        except:
            raise ValueError("Users not found")

        return users

    def fetch_user_by_email(self, email: str) -> Optional[UserReadModel]:
        try:
            user = self.user_query_service.find_by_email(email)
            if user is None:
                raise ValueError("User not found")

        except:
            raise ValueError("User not found")

        return user
