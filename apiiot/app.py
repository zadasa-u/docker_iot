import asyncio
import logging
import os

from db_actions import DbAction
from dispatcher import Dispatcher
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy import URL, MetaData, Table, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(
    format="%(asctime)s - apiiot - %(levelname)s:%(message)s",
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S %z",
)

app = FastAPI()
# db_actor: DbAction = DbAction()
agent: Dispatcher = None


@app.on_event("startup")
async def initialize_model() -> None:
    global agent
    agent = await Dispatcher.factory()


@app.get("/ultimos")
async def ultima():
    result = await agent.get_ultimas_mediciones()
    return jsonable_encoder(result)
