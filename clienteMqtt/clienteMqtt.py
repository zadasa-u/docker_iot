import asyncio, ssl, certifi, logging
import aiomqtt
from environs import Env

env = Env()
env.read_env() #lee el archivo con las variables. por defecto .env

TP = int(env("TP"))

logging.basicConfig(format='%(asctime)s - cliente mqtt - %(levelname)s:%(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S')

contador = 0

async def task():
    global contador
    while True:
        contador += 1
        logging.info('coro: task - ' + 'count: ' + str(contador))
        await asyncio.sleep(3)

async def receive(client):
    await client.subscribe(env("TOPICO1"))
    await client.subscribe(env("TOPICO2"))
    async for message in client.messages:
        logging.info('coro: receive - ' + str(message.topic) + ": " + message.payload.decode("utf-8"))

async def publish(client):
    global contador
    while True:
        await client.publish(env("PUBLICAR"), str(contador))
        logging.info('coro: publish - ' + 'topic: ' + env("PUBLICAR") + ' - payload: ' + str(contador))
        await asyncio.sleep(TP)

async def main():
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

    async with aiomqtt.Client(
        env("SERVIDOR"),
        port=8883,
        tls_context=tls_context,
    ) as client:
        await asyncio.gather(receive(client),publish(client), task())

if __name__ == "__main__":
    asyncio.run(main())
