
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, DateTime, Column, Integer,String, ForeignKey,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from main.db import Base



class Role(Base):
    __tablename__ = 'admin_role'
    id = Column(Integer(), primary_key=True,autoincrement="auto")
    name = Column(String(80), unique=True)
    description = Column(String(255))
    users=relationship("User",secondary='admin_roles_users',back_populates="roles",lazy="selectin")
    content_read_roles=relationship('ContentTypes',secondary='admin_content_type_read_roles',back_populates='read_roles')
    content_write_roles=relationship('ContentTypes',secondary='admin_content_type_write_roles',back_populates='write_roles')      
    
    def __str__(self):
        return f"{self.name}"
    
class User(Base):
    """ User Model for storing user related details """
    __tablename__ = "admin_user"
    id = Column(Integer(), primary_key=True,autoincrement="auto")
    uid=Column(String(36),unique=True,default=uuid.uuid4())
    email=Column(String(255), unique=True,nullable=False)
    username =Column(String(100),unique=True,nullable=False)
    first_name =Column(String(100),nullable=False)
    middle_name = Column(String(100),nullable=False)
    last_name= Column(String(100),nullable=False)
    password = Column(String(500),nullable=False)
    date_registerd=Column(DateTime(timezone=True), default=func.now())
    disabled = Column(Boolean(),default=False)
    roles = relationship('Role', secondary='admin_roles_users',cascade="all, delete",back_populates="users",lazy='joined')
     
    def __str__(self):
        return f"{self.email}"


class RolesUsers(Base):
    __tablename__ = 'admin_roles_users'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column('user_id', Integer(),ForeignKey('admin_user.id',ondelete="CASCADE"),nullable=False)
    role_id = Column('role_id', Integer(), ForeignKey('admin_role.id',ondelete="CASCADE"),nullable=False)
    UniqueConstraint(user_id,role_id)
    
    def __str__(self):
        return f"<UserRole '{self.id}'>"
    
 
class ContentTypes(Base):
    __tablename__='admin_content_type'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    app_label =Column(String(50),nullable=False)
    model_name =Column(String(50),nullable=False)
    read_roles=relationship('Role',secondary='admin_content_type_read_roles',back_populates='')
    write_roles=relationship('Role',secondary='admin_content_type_write_roles',back_populates='')

    def __str__(self):
        return f"{self.model_name}-{self.app_label}"

    def get_read_roles(self):
        return self.read_roles
    
    def get_write_roles(self):
        return self.write_roles
        
class ContentTypeReadRoles(Base):
    __tablename__='admin_content_type_read_roles'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    content_type_id=Column(Integer(),ForeignKey('admin_content_type.id',ondelete="CASCADE"))
    content_role_id=Column(Integer(),ForeignKey('admin_role.id',ondelete="CASCADE"))
    

class ContentTypeWriteRoles(Base):
    __tablename__='admin_content_type_write_roles'
    id=Column(Integer(),primary_key=True, autoincrement=True)
    content_type_id=Column(Integer(),ForeignKey('admin_content_type.id',ondelete="CASCADE"))
    content_role_id=Column(Integer(),ForeignKey('admin_role.id',ondelete="CASCADE"))
    