import uuid
from datetime import tzinfo, timedelta, datetime
from typing import List, Optional,Literal
from pydantic import BaseModel,EmailStr
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

class RoleModel(BaseModel):
    name : str 
    description : Optional[str]
    class Config:
        orm_mode = True

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
    email:EmailStr      
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

class RoleModelAll(BaseModel):
    id : Optional[int]
    name : Optional[str] 
    description : Optional[str]   
    users : Optional[List[UserModelAll]]=[]
  
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
      
class RolesUsersModel(BaseModel):   
        user_id :int
        role_id : int

class ContentRolesModel(BaseModel):
    name : Optional[str]

    class Config:
        orm_mode=True

class ContentTypesModel(BaseModel):
    id : int
    app_label : int
    model_name : int
    read_roles : List[ContentRolesModel]
    # write_roles : Optional[List[ContentRolesModel]]

    class Config:
        orm_mode=True