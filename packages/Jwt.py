from datetime import datetime, timedelta
from fastapi import Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from config.settings.base import settings

# OAuth2PasswordBearerのusernameとpasswordをemailとpasswordに変更しoauth2_scheme に代入
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="user/login_create_token",
)

"""
x-www-form-urlencoded形式でemailとpasswordに変更したいとき
以下のようにする
"""


class EmailPasswordRequestForm(OAuth2PasswordRequestForm):
    email: str
    password: str
    scopes: str

    def __init__(self, email: str = Form(...), password: str = Form(...), scope: str = Form(default="")):
        super().__init__(username=email, password=password, scope=scope)
        self.email = email
        self.password = self.password


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=15)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload is None:
            raise HTTPException(status_code=400, detail="Invalid token")

    except JWTError:
        # raise credentials_exception
        raise HTTPException(status_code=400, detail="Invalid token")

    return payload
