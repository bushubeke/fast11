
from fastapi import APIRouter,status,Request,Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,delete,text
from sqlalchemy.orm import selectinload,joinedload
from main.db import get_session
from main.roleadmin import check_user_role
from store.models import Customer,Address,Order,OrderItem,Promotion,Product,ProductPromotion,\
        Cart,CartItem,Review
from store.serializers import ProductModel,ProductPromotionModel,PromotionModel,\
    ReviewModel,OrderModel,OrderItemMOdel,CartModel,CartItemModel,\
        CustomerModel,AddressModel,OrderModelAll,ProductModelAll
from user.models import ContentTypes
from user.serializers import ContentTypesModel


store_app=APIRouter()

@store_app.get("/order",response_model=Page[OrderModelAll])
async def get_order(request:Request,session : AsyncSession=Depends(get_session)):
    try: 
        orders=await session.scalars(select(Order).options(selectinload(Order.products)).order_by(Order.id))
        orders=orders.all()
        return paginate(orders)
    except Exception as e:
         return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@store_app.get("/order/{order_id:int}",response_model=OrderModelAll)
async def get_one_order(request:Request,order_id : int,session : AsyncSession=Depends(get_session)):
    try: 
        order=await session.execute(select(Order).where(Order.id==order_id))
        order=order.unique().scalars().first()
        return OrderModelAll.from_orm(order)
    except Exception as e:
         return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@store_app.get("/product",response_model=Page[ProductModelAll])
async def get_some_products(request:Request,session : AsyncSession=Depends(get_session)):
    try: 
        products=await session.scalars(select(Product).options(selectinload(Product.orders)).order_by(Product.id))
        products=products.all()
        return paginate(products)
    except Exception as e:
         return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@store_app.get("/product/{product_id:int}",response_model=ProductModelAll)
async def get_one_product(request:Request,product_id : int,session : AsyncSession=Depends(get_session)):
    try: 
        product=await session.execute(select(Product).where(Product.id==product_id))
        product=product.unique().scalars().first()
        return ProductModelAll.from_orm(product)
    except Exception as e:
         return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@store_app.get("/test")
async def get_test_order(request:Request,session : AsyncSession=Depends(get_session)):
    try: 
        await check_user_role(['superuser'],'store_order')
        return JSONResponse({"Message":"Working Fine"},status_code=status.HTTP_200_OK)
    except Exception as e:
         return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
