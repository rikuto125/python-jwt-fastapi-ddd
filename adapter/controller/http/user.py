from abc import abstractmethod, ABC
from typing import Iterator, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from domain.user.user_repsotory import UserRepository
from driver.rdb import SessionLocal
from infrastructure.mysql.user.user_repository import UserRepositoryImpl, UserCommandUseCaseUnitOfWorkImpl
from packages.Jwt import EmailPasswordRequestForm, oauth2_scheme
from usecase.user.user_command_model import UserCreateModel
from usecase.user.user_usecase import UserCommandUseCase, UserCommandUseCaseUnitOfWork, UserCommandUseCaseImpl

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


class UserController(ABC):
    @abstractmethod
    def get_current_active_user(self, token: str) -> Any:
        pass


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def user_command_usecase(session: Session = Depends(get_session)) -> UserCommandUseCase:
    user_repository: UserRepository = UserRepositoryImpl(session)
    uow: UserCommandUseCaseUnitOfWork = UserCommandUseCaseUnitOfWorkImpl(
        session,
        user_repository,
    )
    return UserCommandUseCaseImpl(uow)


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
)
def create_user(
        user: UserCreateModel,
        user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
):
    try:
        user_command_usecase.create_user(user)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return {'message': 'success'}


@router.post(
    '/login_create_token',
    status_code=status.HTTP_201_CREATED,
)
def login_create_token(
        form_data: EmailPasswordRequestForm = Depends(),
        user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
):
    try:
        login_create_token = user_command_usecase.login_create_token(form_data.email, form_data.password)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # returnでcookieにtokenを保存する
    return {'accsesstoken': login_create_token}


# JWTの認証を行う
def get_current_active_user(
        token: str = Depends(oauth2_scheme),
        user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
):
    try:
        user = user_command_usecase.get_current_user(token)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user


@router.get(
    '/get_me',
    status_code=status.HTTP_200_OK,
)
def get_me(
        current_user: UserCreateModel = Depends(get_current_active_user),
):
    return current_user
