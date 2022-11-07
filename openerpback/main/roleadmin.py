import asyncio
from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from user.models import ContentTypes
from user.serializers import ContentRolesModel,ContentTypesModel
from main.db import sessionmade


async def check_user_role(user_roles : List[str], model_name :str)->bool:
    async with sessionmade() as session:
        obrole=await session.scalars(select(ContentTypes).where(ContentTypes.model_name==model_name) \
                .options(selectinload(ContentTypes.read_roles)) \
                    .options(selectinload(ContentTypes.write_roles)))
        obrole=obrole.first()
        print(obrole)
        ob_roles=[ContentRolesModel.from_orm(x).name for x in obrole.read_roles]
        print(ob_roles)
    return True 