import asyncio, ssl, certifi, logging, sys
import aiomqtt
from environs import Env

env = Env()
env.read_env() #lee el archivo con las variables. por defecto .env

TP = int(env("TP"))

logging.basicConfig(format='%(asctime)s - cliente mqtt - %(taskName)s => %(levelname)s: %(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S')

cuenta = 0

async def task():
    global cuenta
    while True:
        cuenta += 1
        logging.info('Valor contador: ' + str(cuenta))
        await asyncio.sleep(3)

async def receive(client):
    async for message in client.messages:
        logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))

async def publish(client):
    global cuenta
    while True:
        await client.publish(env("PUBLICAR"), str(cuenta))
        logging.info('topic: ' + env("PUBLICAR") + ' - payload: ' + str(cuenta))

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
        await client.subscribe(env("TOPICO1"))
        await client.subscribe(env("TOPICO2"))
        
        async with asyncio.TaskGroup() as tg:
            tg.create_task(receive(client), name='receive')
            tg.create_task(publish(client), name='publish')
            tg.create_task(task(), name='contador')
        
        #await asyncio.gather(receive(client),publish(client), task())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
