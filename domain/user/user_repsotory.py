from abc import ABC, abstractmethod
from typing import Optional

from domain.user.user import User


class UserRepository(ABC):
    """UserRepository defines a repository interface for User entity."""
    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user: User) -> Optional[User]:
        raise NotImplementedError
