import asyncio
import logging
import os

from sqlalchemy import URL, MetaData, Table, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class DbAction:
    def __init__(self) -> None:
        url_object = URL.create(
            "mysql+aiomysql",
            username=os.environ["MARIADB_USER"],
            password=os.environ["MARIADB_USER_PASS"],
            host=os.environ["MARIADB_SERVER"],
            database=os.environ["MARIADB_DB"],
        )
        self.engine = create_async_engine(url_object)
        self.meta = MetaData()
        self.async_session = sessionmaker(self.engine, class_=AsyncSession)
        self.tabla = None  # esto va a ser un dict en el futuro

    async def instantiate_models(self):
        # este metodo tiene que mediante un for crear el
        # dict para mapear todos los modelos de las tablas
        # self.tabla ={
        #       'os.environ["MARIADB_TABLE"]': Table(os.environ["MARIADB_TABLE"]...)
        #   }
        async with self.engine.connect() as conn:
            await conn.run_sync(self.meta.reflect, only=[os.environ["MARIADB_TABLE"]])
            self.tabla = Table(
                os.environ["MARIADB_TABLE"], self.meta, autoload_with=self.engine
            )
