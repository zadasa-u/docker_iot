import asyncio, ssl, certifi, logging, sys, os
import aiomqtt

logging.basicConfig(format='%(asctime)s - cliente mqtt - [%(taskName)s] => %(levelname)s: %(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S')

async def counter():
    cuenta = 0
    while True:
        cuenta += 1
        logging.info('Valor cuenta: ' + str(cuenta))
        cola_conteo.put_nowait(cuenta)
        await asyncio.sleep(3)

async def topic1_consumer():
    while True:
        message = await topic1_queue.get()
        logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))

async def topic2_consumer():
    while True:
        message = await topic2_queue.get()
        logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))

async def distributor(client):
    async for message in client.messages:
        if message.topic.matches(os.environ['TOPICO1']):
            topic1_queue.put_nowait(message)
        elif message.topic.matches(os.environ['TOPICO2']):
            topic2_queue.put_nowait(message)

async def publish(client):

    TP = int(os.environ["TP"])
    
    while True:
        cuenta = await cola_conteo.get()
        await client.publish(os.environ["PUBLICAR"], str(cuenta))
        logging.info('topico: ' + os.environ["PUBLICAR"] + ' - pyload: ' + str(cuenta))

        await asyncio.sleep(TP)

async def main():
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

    async with aiomqtt.Client(
        os.environ["SERVIDOR"],
        port=8883,
        tls_context=tls_context,
    ) as client:
        await client.subscribe(os.environ['TOPICO1'])
        await client.subscribe(os.environ['TOPICO2'])
        
        async with asyncio.TaskGroup() as tg:
            tg.create_task(distributor(client), name='atender mensajes')
            tg.create_task(topic1_consumer(), name='consumir topico 1')
            tg.create_task(topic2_consumer(), name='consumir topico 2')
            tg.create_task(publish(client), name='publicacion')
            tg.create_task(counter(), name='conteo')

if __name__ == "__main__":

    topic1_queue = asyncio.Queue()
    topic2_queue = asyncio.Queue()
    cola_conteo = asyncio.Queue()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
