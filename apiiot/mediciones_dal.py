from db_actions import DbAction
from sqlalchemy import URL, MetaData, Table, select


class MedicionesDAL:
    def __init__(self, db_actor: DbAction) -> None:
        self._db_actor = db_actor

    async def traer_ultimos(self, cantidad_de_mediciones=1):
        async with self._db_actor.async_session() as session:
            resultado = await session.execute(
                select(self._db_actor.tabla).order_by(self._db_actor.tabla.c.id.desc())
            )
            ultimos = resultado.first()
            columnas = [c.name for c in self._db_actor.tabla.columns]
            ultimos_zip = zip(columnas, ultimos)
            # logging.info(ultimos)
            await session.commit()
        return ultimos_zip

    # aca agregar acciones especificas unicamente sobre la tabla mediciones
