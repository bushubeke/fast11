from collections import UserList
from enum import unique
from select import select
from typing import List, Optional,Literal
from sqlalchemy import DateTime, Column, Integer,String, ForeignKey,DECIMAL,UniqueConstraint
from sqlalchemy.orm import relationship,backref
from sqlalchemy.sql import func
from main.db import Base 
from user.models import User as RelationUser

class Customer(Base):
    __tablename__="store_customer"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id=Column(Integer(),ForeignKey(RelationUser.id),unique=True)
    membership=Column(String(1)) # validate using pydantic model(B|S|G)
    orders=relationship('Order',back_populates='customer')
    customer=relationship(RelationUser, backref=backref('customer', uselist=True))


class Address(Base):
    __tablename__="store_address"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    city=Column(String(100))
    customer_id=Column(Integer(),ForeignKey('store_customer.id'))

    def __str__(self):
        return self.city

class Order(Base):
    __tablename__="store_order"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    placed_at=Column(DateTime(timezone=True), default=func.now())
    payment_status=Column(String(1)) # note choices here (P|C|F) ('Pending'|'Completed'|'Failed') 
    customer_id=Column(Integer(),ForeignKey('store_customer.id',ondelete='CASCADE'))
    customer=relationship('Customer', back_populates='orders')
    products=relationship('Product',secondary='store_orderitem',lazy='selectin')

    def __str__(self)->str:
        return f"{self.id}-status:{self.payment_status}"

    def __repr__(self)->str:
        return f"{self.id}-status:{self.payment_status}"
            
class OrderItem(Base):
    __tablename__="store_orderitem"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    unit_price=Column(DECIMAL())
    city=Column(String(100))
    order_id=Column(Integer(),ForeignKey('store_order.id'))
    product=Column(Integer(),ForeignKey('store_product.id'))
    

class Product(Base):
    __tablename__="store_product"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title=Column(String(100),nullable=False)
    description=Column(String(200),nullable=True)
    unit_price=Column(DECIMAL())
    quantity=Column(Integer())
    last_update=Column(DateTime(timezone=True),default=func.now())
    collections=relationship('Collection',back_populates='products')
    reviews=relationship('Review',back_populates='products',lazy='selectin')
    promotions=relationship('Promotion',secondary='store_product_promotion',lazy='selectin')
    orders=relationship(Order,secondary='store_orderitem',lazy='selectin',back_populates='products')

    def __str__(self) -> str:
        return self.title

class Promotion(Base):
    __tablename__="store_promotion"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title=Column(String())
    featured_product_id=Column(Integer(),ForeignKey('store_product.id'))

class ProductPromotion(Base):
    __tablename__="store_product_promotion"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    product_id = Column( Integer(),ForeignKey('store_promotion.id',ondelete="CASCADE"),nullable=False)
    promotion_id = Column(Integer(), ForeignKey('store_product.id',ondelete="CASCADE"),nullable=False)
    UniqueConstraint(product_id,promotion_id)

class Review(Base):
    __tablename__="store_review"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name=Column(String())
    date_reviewed=Column(DateTime(timezone=True),default=func.now())
    product_id=Column(Integer(),ForeignKey('store_product.id'))
    products=relationship('Product')

class Collection(Base):
    __tablename__="store_collection"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title=Column(String())
    featured_product=Column(Integer(),ForeignKey('store_product.id'))
    products=relationship('Product')

class Cart(Base):
    __tablename__="store_cart"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    created_at=Column(DateTime(timezone=True), default=func.now())

class CartItem(Base):
    __tablename__="store_cartitem"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    quantity=Column(Integer())
    cart_id=Column(Integer(),ForeignKey('store_cart.id'))
    product_id=Column(Integer(),ForeignKey('store_product.id'))


