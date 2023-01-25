from typing import Optional

from sqlalchemy.exc import NoResultFound

from domain.user.user import User
from domain.user.user_repsotory import UserRepository
from infrastructure.mysql.user import UserDTO
from usecase.user.user_usecase import UserCommandUseCaseUnitOfWork
from sqlalchemy.orm.session import Session


class UserRepositoryImpl(UserRepository):

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[User]:
        try:
            user_dto = self.session.query(UserDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_entity()

    def find_by_email(self, email: str) -> Optional[User]:
        try:
            user_dto = self.session.query(UserDTO).filter_by(email=email).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_entity()

    def create(self, user: User):
        user_dto = UserDTO.from_entity(user)
        try:
            self.session.add(user_dto)
        except:
            raise

    def update(self, user: User):
        user_dto = UserDTO.from_entity(user)
        try:
            _user = self.session.query(UserDTO).filter_by(id=user_dto.id).one()
            _user.name = user_dto.name
            _user.updated_at = user_dto.updated_at
        except:
            raise

    def delete(self, user: User):
        user_dto = UserDTO.from_entity(user)
        try:
            self.session.delete(user_dto)
        except:
            raise


class UserCommandUseCaseUnitOfWorkImpl(UserCommandUseCaseUnitOfWork):

    def __init__(
            self,
            session: Session,
            user_repository: UserRepository
    ):
        self.session = session
        self.user_repository: UserRepository = user_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
