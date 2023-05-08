
class Dispatcher:
    def __init__(self) -> None:
        db_actor:DbAction = DbAction()
        mediciones_dal = Mediciones_dal(db_actor)
    
    async def get_ultimas_mediciones(self, cantidad):
        resultado = await nodos_dal.traer_ultimos(cantidad)