import asyncio, logging
from fastapi import FastAPI
from sqlalchemy import MetaData, select, URL, Table
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

logging.basicConfig(format='%(asctime)s - apiiot - %(levelname)s:%(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

app = FastAPI(root_path="/api")
url_object = URL.create(
    "mysql+aiomysql",
    username=os.environ["MARIADB_USER"],
    password=os.environ["MARIADB_USER_PASS"],
    host=os.environ["MARIADB_SERVER"],
    database=os.environ["MARIADB_DB"],
)
engine = create_async_engine(url_object)
meta = MetaData()

@app.get("/ultimos")
async def ultima():
    async with engine.connect() as conn:
        await conn.run_sync(meta.reflect, only=[os.environ["MARIADB_TABLE"]])
        tabla = Table(os.environ["MARIADB_TABLE"], meta, autoload_with=engine)
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with async_session() as session:
            resultado = await session.execute(select(tabla).order_by(tabla.c.id.desc()))
            ultimos=resultado.first()
            columnas=[c.name for c in tabla.columns]
            ultimos_zip=zip(columnas,ultimos)
            logging.info(ultimos)
    await engine.dispose()
    return ultimos_zip
    