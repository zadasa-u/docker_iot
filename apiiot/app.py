import logging

from config import Config
from dispatcher import Dispatcher
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s:%(message)s",
    level=Config.LOG_LEVEL,
    datefmt="%d/%m/%Y %H:%M:%S %z",
)


logger = logging.getLogger("app")

app = FastAPI()
app.agent: Dispatcher | None = None


@app.on_event("startup")
async def initialize_model() -> None:
    app.agent = await Dispatcher.factory(Config)
    logger.debug("Dispatcher initiated.")


@app.get("/ultimos")
async def ultima():
    result = await app.agent.get_ultimas_mediciones()
    return jsonable_encoder(result)
