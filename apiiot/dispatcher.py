from db_actions import DbAction
from mediciones_dal import MedicionesDAL


class Dispatcher:
    def __init__(self, db_actor) -> None:
        self._db_actor: DbAction = db_actor
        self.mediciones_dal = MedicionesDAL(self._db_actor)
        # self.nodos_dal = NodosDal(db_actor)
        # self.otro_Dal =

    async def get_ultimas_mediciones(self, cantidad=1):
        ultima_medicion = await self.mediciones_dal.traer_ultimos(cantidad)
        return ultima_medicion

    # en el caso de que haya que hacer alguna union yo las haria aca
