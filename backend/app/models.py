from sqlmodel import Field, Relationship, SQLModel,Column,String



# Shared properties
class UserBase(SQLModel):
    is_active: bool = True
    is_superuser: bool = False
    email :str  = Field(index=True)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    email :str  
    username: str
    full_name:str | None = None
class UserCreateOpen(SQLModel):
    phonenum: str
    username: str
    password: str


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    phonenum: str | None = None  # type: ignore
    password: str | None = None
    full_name:str | None = None

class UserUpdateMe(SQLModel):
    full_name: str | None = None
    phonenum: str | None = None
    email: str |None = None
    

class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    username:str 
    full_name: str | None = Field(default=None, nullable=True)
    
    

# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int
    full_name:str  | None = None
    

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
    pass
