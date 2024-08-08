from datetime import datetime, timezone
from uuid import UUID, uuid4
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
class PersonalInformation(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    job_number:str
    name:str
    sex:str
    birthday:str
    age:str
    marital_status:str
    identity_card_number:str
    nation:str
    political_status:str
    native_place:str
    place_of_domicile:str  
    initial_education:str   #初始学历
    highest_degree:str    #最高学历
    diploma_kind: str   # 全日制或非全日制
    teaching_title:str  #教学职称
    foreign_language:str
    credit_card_number:str #学分卡号
    health_condition:str
    strong_point:str
class CommunicationInformation(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    phone_number:str
    work_phone:str
    contact_name:str
    contact_number:str
    contact_relationship:str #联系人关系
    mailing_address:str
    postal_code:str #邮政编码

class JobInformation(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    category:str
    professional_group:str
    personal_relations_belong_to_unit:str  #人事关系单位属
    job:str
    on_book_status:str #在编情况
    on_the_job_status:str #在职情况
    title:str #职称
    title_level:str
    title_major:str
    acquisition_time:str
class UpdateUserInfoLog(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    updated_at: datetime = Field(default=datetime.now(timezone.utc)) #TODO: complete me
    changed_column: str
    changed_table: str 
    old_value: str
    new_value: str
    update_uuid: UUID=Field(default=uuid4)  #TODO: uuid  column 
    user_id: int
    operate_user_id: int 