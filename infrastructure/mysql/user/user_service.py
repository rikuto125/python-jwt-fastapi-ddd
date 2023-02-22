from abc import ABC
from typing import Optional

from sqlalchemy.exc import NoResultFound

from domain.user.user import User
from infrastructure.mysql.user import UserDTO
from sqlalchemy.orm.session import Session

from usecase.user.user_query_service import UserQueryService


class UserQueryServiceImpl(UserQueryService):
    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[User]:
        try:
            user_dto = self.session.query(UserDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_read_model()

    def find_by_email(self, email: str) -> Optional[User]:
        try:
            user_dto = self.session.query(UserDTO).filter_by(email=email).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_read_model()

    def find_all(self):
        try:
            user_dtos = (
                self.session.query(UserDTO)
                .order_by(UserDTO.updated_at)
                .limit(100)
                .all()
            )
        except:
            raise

        if len(user_dtos) == 0:
            return []

        return list(map(lambda user_dto: user_dto.to_read_model(), user_dtos))
