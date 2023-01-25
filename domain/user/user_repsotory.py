from abc import ABC, abstractmethod
from typing import Optional

from domain.user.user import User


class UserRepository(ABC):
    """BookRepository defines a repository interface for Book entity."""

    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        raise NotImplementedError

    def find_by_id(self, id: str) -> Optional[User]:
        raise NotImplementedError

    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    # def update(self, user: User) -> Optional[User]:
    #     raise NotImplementedError
