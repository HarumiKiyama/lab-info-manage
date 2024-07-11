from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    phonenum: str = Field(unique=True, index=True)
    username: str
    is_active: bool = True
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


class UserCreateOpen(SQLModel):
    phonenum: str
    username: str
    password: str


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    phonenum: str | None = None  # type: ignore
    password: str | None = None


class UserUpdateMe(SQLModel):
    full_name: str | None = None
    phonenum: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    hashed_password: str

# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str

class Message(SQLModel):
    message: str
