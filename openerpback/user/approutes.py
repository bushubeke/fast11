
import jwt
from datetime import datetime,timedelta
from fastapi import APIRouter, Depends,HTTPException, status,Request
from fastapi_pagination import Page, paginate
# from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from passlib.hash import pbkdf2_sha512
from sqlalchemy import select,update,delete
from sqlalchemy.orm import joinedload,selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from main.db import get_session
from user.utils import *
from user.models import *
from store.models import Product,Order
from user.serializers import *


###########################################################
auth = APIRouter()
##########################################################


@auth.post("/user")
async def add_new_user(reqest:Request,user : UserModel, session : AsyncSession=Depends(get_session)):
    data=dict(user)
    data['uid']=str(uuid.uuid4())
    
    return UserModelAll.from_orm(User(**data))

@auth.get('/user/{user_id:int}',response_model=UserModelAll)
async def get_one_user(request : Request,user_id : int,session : AsyncSession=Depends(get_session)):
	try:
		print(select(Order))
		user=await session.execute(select(User).where(User.id==user_id).options(joinedload(User.roles)))
		return UserModelAll.from_orm(user.unique().scalars().first())
	except Exception as e:
			JSONResponse({"Message" : str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
	finally:
		await session.close()
@auth.get('/user',response_model=Page[UserModelAll])
async def get_some_user(request : Request,session : AsyncSession=Depends(get_session)): 
	try:
		users=await session.execute(select(User).options(joinedload(User.roles)).order_by(User.id))
		users=users.unique().scalars().all()
		return paginate(users)
	except Exception as e:
			JSONResponse({"Message" : str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
	finally:
		await session.close()
@auth.get('/role/{role_id:int}',response_model=RoleModelAll)
async def get_one_user(request : Request,role_id : int,session : AsyncSession=Depends(get_session)):
	try:
		role=await session.execute(select(Role).where(Role.id==role_id).options(selectinload(Role.users)))
		return RoleModelAll.from_orm(role.unique().scalars().first())
	except Exception as e:
		JSONResponse({"Message" : str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
	finally:
		await session.close()
		
@auth.get('/role',response_model=Page[RoleModelAll])
async def get_some_user(request : Request,session : AsyncSession=Depends(get_session)): 
	try:
			roles=await session.execute(select(Role).options(selectinload(Role.users)).order_by(Role.id))
			roles=roles.unique().scalars().all()
			return paginate(roles)
	except Exception as e:
			JSONResponse({"Message" : str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
	finally:
		await session.close()
@auth.post("/login")
async def login_user(request : Request ,session :AsyncSession=Depends(get_session)):
    # logdata=dict(login_data)
    try:
            return {"access_token": "something", "token_type": "bearer"}
            # if logdata['grant_type'] =='authorization_code':
            #     user=await session.execute(select(User).filter_by(username=logdata['username']).options(joinedload(User.roles)))
            #     user=user.unique().scalars().first()
            #     data=dict(UserModelAll.from_orm(user))
            #     #handling data for nested pydantic and datacalss objects
            #     data=dataclass_to_dic(data)
            #     data=uuid_to_str(data)
            #     if  pbkdf2_sha512.verify(logdata['password'],data["password"]):                        
            #         exp=datetime.utcnow()+timedelta(hours=settings.JWT_APP_TOKEN_EXPIRE_TIME)
            #         exp2=datetime.utcnow()+timedelta(hours=settings.JWT_REFRESH_TOKEN_EXPIRE_TIME)
            #         key=settings.SECRET_KEY 
            #         del data["password"]
            #         del data["date_registerd"]
            #         token=jwt.encode({"data":data,"exp":exp,},key,algorithm="HS256")
            #         reftoken=jwt.encode({'data':data,'exp':exp2},key,algorithm="HS256")
            #         return JSONResponse({"access_token": token,"refresh_token":reftoken, "token_type": "bearer"},status_code=status.HTTP_202_ACCEPTED)
            #     return JSONResponse({"Message":"Invalid Password"},status_code=status.HTTP_401_UNAUTHORIZED)
            # elif logdata['grant_type'] == "refresh_token":
            #         exp=datetime.utcnow()+timedelta(hours=4)
            #         exp2=datetime.utcnow()+timedelta(hours=5)
            #         key=settings.SECRET_KEY
            #         data=jwt.decode(logdata['token'],key,algorithms="HS256")
            #         data=data["data"]
            #         token=jwt.encode({'data':data,'exp':exp},key,algorithm="HS256")
            #         reftoken=jwt.encode({'data':data,'exp':exp2},key,algorithm="HS256")
            #         return JSONResponse({"access_token": token,"refresh_token":reftoken, "token_type": "bearer"},status_code=status.HTTP_202_ACCEPTED)
            # elif logdata['grant_type'] == "token_decode":
            #         key=settings.SECRET_KEY
            #         data=jwt.decode(logdata['token'],key,algorithms="HS256")
            #         return JSONResponse(data["data"],status_code=status.HTTP_206_PARTIAL_CONTENT)
            # else:
            #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Message: Something Unexpected Happended")
    finally:
            await session.close()
