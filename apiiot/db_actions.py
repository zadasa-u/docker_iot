import logging

from config import Config
from sqlalchemy import Table

logger = logging.getLogger("app.dispatcher." + __name__)


class DbAction:
    def __init__(self, engine, meta, async_session, tablas) -> None:
        self.engine = engine
        self.meta = meta
        self.async_session = async_session
        self.tablas = tablas

    @staticmethod
    async def instantiate_models(engine, meta):
        # mediante un for crea el dict para mapear todos
        # los modelos de todas las tablas
        # tabla = {
        #       'mediciones': Table(...)
        #   }

        # async with engine.connect() as conn:
        #    await conn.run_sync(meta.reflect, only=[os.environ["MARIADB_TABLE"]])
        #    tabla = Table(os.environ["MARIADB_TABLE"], meta, autoload_with=engine)
        # logger.debug("Model for table %s is ready", tabla)
        # return tabla

        table_model_map = {}
        async with engine.connect() as conn:
            for t in Config.MARIADB_DB_TABLES_LIST:
                await conn.run_sync(meta.reflect, only=[t])
                table_model_map[t] = Table(t, meta, autoload_with=engine)
                logger.debug("Model for table %s is ready", t)

        return table_model_map
