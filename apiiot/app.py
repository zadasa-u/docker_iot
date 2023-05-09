import logging

from dispatcher import Dispatcher
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

logging.basicConfig(
    format="%(asctime)s - apiiot - %(levelname)s:%(message)s",
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S %z",
)

app = FastAPI()
app.agent = None


@app.on_event("startup")
async def initialize_model() -> None:
    app.agent = await Dispatcher.factory()


@app.get("/ultimos")
async def ultima():
    result = await app.agent.get_ultimas_mediciones()
    return jsonable_encoder(result)
