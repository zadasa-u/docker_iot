import os

from db_actions import DbAction
from mediciones_dal import MedicionesDAL
from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class Dispatcher(DbAction):
    def __init__(self, engine, meta, async_session, tabla) -> None:
        super().__init__(engine, meta, async_session, tabla)

        self.mediciones_dal = MedicionesDAL(self.async_session, self.tabla)
        # self.nodos_dal = NodosDal(db_actor)
        # self.otro_dal =

    async def get_ultimas_mediciones(self, cantidad=1):
        ultima_medicion = await self.mediciones_dal.traer_ultimos(cantidad)
        return ultima_medicion

    @classmethod
    async def factory(cls):
        url_object = URL.create(
            "mysql+aiomysql",
            username=os.environ["MARIADB_USER"],
            password=os.environ["MARIADB_USER_PASS"],
            host=os.environ["MARIADB_SERVER"],
            database=os.environ["MARIADB_DB"],
        )
        engine = create_async_engine(url_object)
        meta = MetaData()
        async_session = sessionmaker(engine, class_=AsyncSession)
        tabla = await super().instantiate_models(engine, meta)
        return cls(engine, meta, async_session, tabla)

    # en el caso de que haya que hacer alguna union yo las haria
    # aca dentro del Dispatcher
