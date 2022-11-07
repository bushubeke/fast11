from datetime import datetime
from typing import Literal,List,Optional
from unicodedata import decimal
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from store.models import Customer,Address,Product,ProductPromotion,Cart,CartItem,Order,OrderItem,Review,Collection,Promotion

CustomerModel=sqlalchemy_to_pydantic(Customer)
ProductModel=sqlalchemy_to_pydantic(Product)
AddressModel=sqlalchemy_to_pydantic(Address)
PromotionModel=sqlalchemy_to_pydantic(Promotion)
ProductPromotionModel=sqlalchemy_to_pydantic(ProductPromotion)
CartModel=sqlalchemy_to_pydantic(Cart)
CartItemModel=sqlalchemy_to_pydantic(CartItem)
OrderModel=sqlalchemy_to_pydantic(Order)
OrderItemMOdel=sqlalchemy_to_pydantic(OrderItem)
ReviewModel=sqlalchemy_to_pydantic(Review)
CollectionModel=sqlalchemy_to_pydantic(Collection)

class OrderModelAll(BaseModel):
    id :int
    placed_at : datetime
    payment_status : Literal['G','S','B']
    customer_id : int
    products : List[ProductModel]=[]
    class Config:
        orm_mode=True


class ProductModelAll(BaseModel):
    id: int
    title:str
    description:str
    unit_price:float 
    quantity: int 
    last_update:datetime
    orders : List[OrderModel]=[]

    class Config:
        orm_mode=True
