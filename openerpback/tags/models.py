import uuid
from datetime import tzinfo, timedelta, datetime
from typing import List, Optional,Literal
from sqlalchemy import Boolean, DateTime, Column, Integer,String, ForeignKey, Sequence,Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel,EmailStr
from main.db import Base

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True,autoincrement="auto")
    name = Column(String(80), unique=True)
    description = Column(String(255))
    users=relationship("User",secondary='roles_users',back_populates="roles")
      
    def __repr__(self):
        return f"{self.name}"
    
    def asdict(self,):
        return self.__dict__
    
    @staticmethod
    def tableroute():
        return "role"
    
    @staticmethod
    def roles_required():
        return ['superuser']
class RoleModel(BaseModel):
    name : str 
    description : Optional[str]
    class Config:
        orm_mode = True
class RoleModelAll(BaseModel):
    id : Optional[int]
    name : Optional[str] 
    description : Optional[str]   
    class Config:
        orm_mode = True

class User(Base):
    """ User Model for storing user related details """
    __tablename__ = "user"
    id = Column(Integer(), primary_key=True,autoincrement="auto")
    # uid = Column(UUID(as_uuid=True),unique=True,default=uuid.uuid4)
    email=Column(String(255), unique=True,nullable=False)
    username =Column(String(100),unique=True,nullable=False)
    first_name =Column(String(100),nullable=False)
    middle_name = Column(String(100),nullable=False)
    last_name= Column(String(100),nullable=False)
    password = Column(String(500),nullable=False)
    date_registerd=Column(DateTime(timezone=True), default=func.now())
    disabled = Column(Boolean(),default=False)
    roles = relationship('Role', secondary='roles_users',cascade="all, delete",back_populates="users")
     
    def __repr__(self):
        return f"<User '{self.username}'>"

    def asdict(self,):
        return self.__dict__
    
    @staticmethod
    def tableroute():
        return "user"
    
    @staticmethod
    def roles_required():
        return ['superuser']

class UserModel(BaseModel):
    email : EmailStr 
    username: str
    first_name : str
    middle_name : Optional[str] = None 
    last_name : str 
    password : str 
    disabled :Optional[bool] 
    class Config:
        orm_mode = True

class LoginUserModel(BaseModel):
    grant_type :Literal['password','authorization_code','refresh_token','token_decode']="authorization_code"
    username:str      
    password :str
    token: Optional[str]='none'

class UserModelAll(BaseModel):
    id : Optional[int] 
    uid : Optional[uuid.UUID]
    email : Optional[EmailStr] 
    username: Optional[str]
    first_name : Optional[str]
    middle_name : Optional[str] = None 
    last_name : Optional[str] 
    password : Optional[str] 
    date_registerd : Optional[datetime]
    disabled :Optional[bool] 
    roles : Optional[List[RoleModel]] = []
    class Config:
        orm_mode = True        

class UserModelLogin(BaseModel):
    id : Optional[int] 
    uid : Optional[uuid.UUID]
    email : Optional[EmailStr] 
    username: Optional[str]
    first_name : Optional[str]
    middle_name : Optional[str] = None 
    last_name : Optional[str] 
    disabled :Optional[bool] 
    roles : Optional[List[RoleModel]] = []
    
class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(),ForeignKey('user.id'),nullable=False)
    role_id = Column('role_id', Integer(), ForeignKey('role.id'),nullable=False)
    #users = relationship('User',backref=backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return f"<UserRole '{self.role_id}'>"
    
    def asdict(self,):
        return self.__dict__
    
    @staticmethod
    def roles_required():
        return ['superuser']

class RolesUsersModel(BaseModel):
      
        user_id :int
        role_id : int


