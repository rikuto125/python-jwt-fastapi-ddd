from fastapi import APIRouter, Depends
from starlette import status

from adapter.controller.http.user import get_current_active_user

router = APIRouter(
    prefix='/book',
    tags=['book'],
)


@router.get(
    '/test',
    status_code=status.HTTP_200_OK,
)
async def test(
        a=Depends(get_current_active_user),
):
    print(a)
    return {'message': 'success'}
