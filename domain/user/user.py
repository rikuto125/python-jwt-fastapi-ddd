from typing import Optional

from pydantic import EmailStr


class User:

    def __init__(self,
                 id: str,
                 name: str,
                 email: str,
                 hashed_password: str,
                 created_at: Optional[int] = None,
                 updated_at: Optional[int] = None,
                 ):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.created_at = created_at
        self.updated_at = updated_at


