import logging

from config import Config
from db_initializer import DbInitializer
from mediciones_dal import MedicionesDAL
from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("app." + __name__)


class Dispatcher(DbInitializer):
    def __init__(self, engine, meta, async_session, tablas) -> None:
        super().__init__(engine, meta, async_session, tablas)

        self.mediciones_dal = MedicionesDAL(
            self.async_session, self.tablas["mediciones"]
        )
        # self.nodos_dal = NodosDal(self.async_session, self.tablas['nodos'])
        # self.otro_dal = OtroDal(self.async_session, self.tablas['otra'])

    async def get_ultimas_mediciones(self, cantidad=1):
        ultima_medicion = await self.mediciones_dal.traer_ultimos(cantidad)
        return ultima_medicion

    @classmethod
    async def factory(cls, config: Config):
        logger.debug(
            "Factory method is instantiating the table models and the Dispatcher"
        )
        url_object = URL.create(
            "mysql+aiomysql",
            username=config.MARIADB_USER,
            password=config.MARIADB_USER_PASS,
            host=config.MARIADB_SERVER,
            database=config.MARIADB_DB,
        )
        engine = create_async_engine(url_object)
        meta = MetaData()
        async_session = sessionmaker(engine, class_=AsyncSession)
        tablas = await super().instantiate_models(engine, meta)
        return cls(engine, meta, async_session, tablas)

    # en el caso de que haya que hacer alguna union yo las haria
    # aca dentro del Dispatcher
