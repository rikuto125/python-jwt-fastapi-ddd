from abc import abstractmethod, ABC
from typing import List, Optional

from domain.user.user_repsotory import UserRepository
from usecase.user.user_query_model import UserReadModel


class UserQueryService(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[UserReadModel]:
        raise NotImplementedError
