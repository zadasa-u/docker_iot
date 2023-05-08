import asyncio, logging
from sqlalchemy import MetaData, select, URL, Table
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

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

    async def instantiate_model(self) -> Table:
        async with self.engine.connect() as conn:
            await conn.run_sync(self.meta.reflect, only=[os.environ["MARIADB_TABLE"]])
            model = Table(os.environ["MARIADB_TABLE"], self.meta, autoload_with=self.engine)
            return model