import logging
import os

from sqlalchemy import Table


class DbAction:
    def __init__(self, engine, meta, async_session, tabla) -> None:
        self.engine = engine
        self.meta = meta
        self.async_session = async_session
        self.tabla = tabla  # esto va a ser un dict en el futuro

    @staticmethod
    async def instantiate_models(engine, meta):
        # este metodo tiene que mediante un for crear el
        # dict para mapear todos los modelos de las tablas
        # tabla = {
        #       'os.environ["MARIADB_TABLE"]': Table(os.environ["MARIADB_TABLE"]...)
        #   }
        async with engine.connect() as conn:
            await conn.run_sync(meta.reflect, only=[os.environ["MARIADB_TABLE"]])
            tabla = Table(os.environ["MARIADB_TABLE"], meta, autoload_with=engine)
        logging.debug("Table models instantiated: %s", tabla)
        return tabla
