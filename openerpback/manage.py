import typer
import asyncio
import subprocess
from tqdm import tqdm
from pathlib import Path
from sqlalchemy import delete,text
from sqlalchemy.sql import text as stext
import psycopg
from main.main import create_dev_app
from main.db import async_main,sessionmade,Base,engine
from user.models import *
from store.models import *
from config import settings

path=Path(__file__).parent    
capp = typer.Typer()
app=create_dev_app()

@capp.command()
def rung():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:9000 with one worker
    """
    subprocess.run(["gunicorn", "manage:app", "-k" ,"uvicorn.workers.UvicornWorker","-b" ,"0.0.0.0:9000","--reload","-w","1"]) 

@capp.command()
def upgrade():
    """creates  base models based on their methadata"""
    asyncio.run(async_main())

@capp.command()
def updatecontents():
    async def upcon():  
        async with sessionmade() as session:
            async with session.begin():
                await session.execute(delete(ContentTypes))
                conts= [(x.split('_')[0],x) for x in Base.metadata.tables.keys() ]
                session.add_all([ContentTypes(app_label=x[0],model_name=x[1]) for x in conts ])
    asyncio.run( upcon()) 


@capp.command()
def dropall():
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import (   DropConstraint,DropTable,MetaData,Table,ForeignKeyConstraint )
    with engine.connect() as con:
        inspector = Inspector.from_engine(engine)
        # We need to re-create a minimal metadata with only the required things to
        # successfully emit drop constraints and tables commands for postgres (based
        # on the actual schema of the running instance)
        meta = MetaData()
        tables = []
        all_fkeys = []
        for table_name in inspector.get_table_names():
            fkeys = []
            for fkey in inspector.get_foreign_keys(table_name):
                if not fkey["name"]:
                    continue
                fkeys.append(ForeignKeyConstraint((), (), name=fkey["name"]))
            tables.append(Table(table_name, meta, *fkeys))
            all_fkeys.extend(fkeys)
        for fkey in all_fkeys:
            con.execute(DropConstraint(fkey))
        for table in tables:
            con.execute(DropTable(table)) 
        con.commit()
@capp.command()
def test(location):
    """
      Takes location of test locations as arguments. this argument is required    
    """
    subprocess.run(["pytest", location,"--asyncio-mode=strict"])

@capp.command()
def usesql(): 
    # using sync sqlalchemy engine
    with engine.connect() as con:
         with open('storedb2.sql') as f:
            for line in tqdm(f.readlines()):
                con.execute(stext(line))
   
    #using psycopg cursor directly when using postgresql
    # conn_dict =  psycopg.conninfo.conninfo_to_dict(settings.PG_URL)
    # with psycopg.connect(**conn_dict) as conn:
    #     with conn.cursor() as cur:
    #         with open('storedb1.sql') as f:
    #             for line in tqdm(f.readlines()):
    #                  conn.execute(line)
                    
                
@capp.command()
def teststmt():
    pass
if __name__ == "__main__":
    capp()  