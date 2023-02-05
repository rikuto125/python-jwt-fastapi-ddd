from fastapi import APIRouter, Depends
from starlette import status
from packages.Jwt import verify_token

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.get(
    '/check_auth',
    status_code=status.HTTP_200_OK,
)
async def auth(
        authenticate=Depends(verify_token),
):
    print(authenticate)
    return {'message': 'success'}
