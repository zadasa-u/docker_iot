class MedicionesDAL:
    def __init__(self, db_actor: DbAction) -> None:
        self.__actor = db_actor
    async def traer_ultimos(self, cantidad_de_mediciones=100):
        async with db_actor.async_session() as session:
            resultado = await session.execute(select(tabla).order_by(tabla.c.id.desc()))
            ultimos=resultado.first()
            columnas=[c.name for c in tabla.columns]
            ultimos_zip=zip(columnas,ultimos)
            logging.info(ultimos)
            await session.commit()
        return ultimos