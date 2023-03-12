from typing import Optional, Union

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    password: str


class UserExists(BaseModel):
    username: str


class UserLogin(UserBase):
    type: str
    autoLogin: bool


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    fullName: str
    roleName: Union[str, int] = None  # 特殊情况,前端回传的实际是 roles表的id 或者 roleName
    verifyKey: str


# Properties to receive via API on update
class UserUpdatePassword(BaseModel):
    passwordOld: str
    passwordNew: str
    verifyKey: str


class UserUpdate(UserCreate):
    id: int


class UserDelete(BaseModel):
    id: int


class UserSetSuperuser(BaseModel):
    id: int
    isSuperuser: int


class UserSetActive(BaseModel):
    id: int
    isActive: int


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashedPassword: str
