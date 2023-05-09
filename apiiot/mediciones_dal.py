import logging

from db_actions import DbAction
from sqlalchemy import URL, MetaData, Table, select


class MedicionesDAL:
    def __init__(self, async_session, tabla) -> None:
        self.async_session = async_session
        self.tabla = tabla
        # logging.warning("MODELOS %s", self.tabla.columns)

    async def traer_ultimos(self, cantidad_de_mediciones=1):
        async with self.async_session() as session:
            resultado = await session.execute(
                select(self.tabla).order_by(self.tabla.c.id.desc())
            )
            ultimos = resultado.first()
            columnas = [c.name for c in self.tabla.columns]
            ultimos_zip = zip(columnas, ultimos)
            logging.debug("The last values are %s", ultimos_zip)
            await session.commit()
        return ultimos_zip

    # aca agregar acciones especificas unicamente sobre la tabla mediciones
