from typing import Iterator
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic.validators import timedelta
from sqlalchemy.orm import Session
from starlette import status

from domain.user.user_repsotory import UserRepository
from driver.rdb import SessionLocal
from infrastructure.mysql.user.user_repository import UserRepositoryImpl, UserCommandUseCaseUnitOfWorkImpl
from infrastructure.mysql.user.user_service import UserQueryServiceImpl
from packages.Jwt import EmailPasswordRequestForm, verify_token
from usecase.user.user_command_model import UserCreateModel
from usecase.user.user_command_usecase import UserCommandUseCase, UserCommandUseCaseUnitOfWork, UserCommandUseCaseImpl
from usecase.user.user_query_service import UserQueryService
from usecase.user.user_query_usecase import UserQueryUseCase, UserQueryUseCaseImpl

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


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


def user_query_usecase(session: Session = Depends(get_session)) -> UserQueryUseCase:
    user_query_service: UserQueryService = UserQueryServiceImpl(session)
    return UserQueryUseCaseImpl(user_query_service)


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
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
async def login_create_token(
        response: Response,
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

    # Bearerトークンをクッキーに保存
    response.set_cookie(
        key='access_token',
        value="Bearer " + login_create_token,
        httponly=True,
        max_age=timedelta(minutes=30),
    )

    return {'token': login_create_token}
    #return {'message': 'success'}


@router.get(
    '/get_me',
    status_code=status.HTTP_200_OK,
)
async def get_me(
        payload: dict = Depends(verify_token),
        user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
):
    try:
        user = user_query_usecase.fetch_user_by_email(payload.get("sub"))

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user
