from datetime import datetime, timezone
from typing import Any, Optional, Type
from models import UpdateUserInfoLog
from sqlmodel import Session, select,SQLModel
from fastapi import HTTPException
from app.core.security import get_password_hash, verify_password
from app.models import  User, UserCreate, UserUpdate
from typing import Dict


def create_user(*, session: Session, user_create: UserCreate) -> User:
    existing_user = session.query(User).filter_by(email=user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_phonenum(*, session: Session, phonenum: str) -> User | None:
    statement = select(User).where(User.phonenum == phonenum)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    db_user = get_user_by_username(session=session, username=username)
    
    if not db_user:      
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def get_user_by_username(*,session:Session, username:str) ->User | None:
    statement= select(User).where(User.username==username)
    session_user=session.exec(statement).first()
    return session_user

def get_user_by_email(*,session:Session,email:str)->User | None:
    statement= select(User).where(User.email==email)
    session_user=session.exec(statement).first()
    return session_user


def add_information(session: Session, model: SQLModel) -> SQLModel:
     session.add(model)
     session.commit()
     session.refresh(model)
     return model

def update_information(session: Session, model: SQLModel, update_data: Dict) -> SQLModel:
    model_data = get_information_by_id(session, model, model.id)
    if model_data:
        for key, value in update_data.items():
            setattr(model_data, key, value)
        session.commit()
        # 记录修改信息
        log = UpdateUserInfoLog(
            table_name=model.__name__,
            record_id=model_data.id,
            change_type='UPDATE',
            change_details=update_data,
            changed_at=datetime.now(timezone.utc)
        )
        session.add(log)
        session.commit()
    return model_data

# 读取记录
def get_information_by_id(session: Session, model: Type[SQLModel], record_id: int) -> Optional[SQLModel]:
    return session.get(model, record_id)