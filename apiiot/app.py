import asyncio, logging
from fastapi import FastAPI
from sqlalchemy import MetaData, select, URL, Table
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from db_actions import DbAction


logging.basicConfig(format='%(asctime)s - apiiot - %(levelname)s:%(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

app = FastAPI()
tabla = None

db_actor:DbAction = DbAction()
agent: Dispatcher = Dispatcher()

@app.on_event("startup")
async def initialize_model() -> None:
    global tabla
    tabla = await db_actor.instantiate_model()


@app.get("/ultimos")
async def ultima():
    #async_session = sessionmaker(engine, class_=AsyncSession)
    async with db_actor.async_session() as session:
        resultado = await session.execute(select(tabla).order_by(tabla.c.id.desc()))
        ultimos=resultado.first()
        columnas=[c.name for c in tabla.columns]
        ultimos_zip=zip(columnas,ultimos)
        logging.info(ultimos)
        await session.commit()
    #await engine.dispose()
    return ultimos_zip
