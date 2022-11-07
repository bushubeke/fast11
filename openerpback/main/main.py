import imp
from fastapi import FastAPI,Header,Depends
from fastapi.security import oauth2
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqladmin import Admin
from main.db import engine,asyncengine
from main.utils import OAuth2AppBearer
from user.approutes import auth
from store.approutes import store_app
from user.admin import UserAdmin,RoleAdmin,ContentTypesAdmin
from user.models import User
def create_dev_app():
    
    app=FastAPI(title="Development User Admin App",debug=False)
    origins = [ "*"]
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )
    tok_bear=OAuth2AppBearer(tokenUrl="/auth/login")
    app.include_router(auth,prefix="/auth")
    app.include_router(store_app,prefix="/store")
    admin=Admin(app,asyncengine,title="Store Admin Dashboard")
    @app.get("/")
    def index(current_user : str=Depends(tok_bear)):
        return {"Message":current_user}
    add_pagination(app)
    admin.add_view(UserAdmin)
    admin.add_view(RoleAdmin)
    admin.add_view(ContentTypesAdmin)
  
    return app

def create_testing_app():
    app=FastAPI()   
    origins = [ "*"]
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )
   
    
    @app.get("/")
    def index():
        return {"Message":"You should make your own index page"}
    return app
