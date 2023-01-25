from typing import Iterator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from domain.user.user_repsotory import UserRepository
from driver.rdb import SessionLocal
from infrastructure.mysql.user.user_repository import UserRepositoryImpl, UserCommandUseCaseUnitOfWorkImpl
from usecase.user.user_command_model import UserCreateModel
from usecase.user.user_usecase import UserCommandUseCase, UserCommandUseCaseUnitOfWork, UserCommandUseCaseImpl

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
