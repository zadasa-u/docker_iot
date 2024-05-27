import asyncio, ssl, certifi, logging, os, aiomysql, json, traceback
<<<<<<< HEAD
from asyncio_mqtt import Client, ProtocolVersion
=======
import aiomqtt
>>>>>>> 0a2284b9291a9de08687c1b3f35ad806e392dfa0

logging.basicConfig(format='%(asctime)s - cliente mqtt - %(levelname)s:%(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

async def main():

    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

<<<<<<< HEAD

    async with Client(
        os.environ["SERVIDOR"],
        username=os.environ["MQTT_USR"],
        password=os.environ["MQTT_PASS"],
        protocol=ProtocolVersion.V31,
        port=8883,
=======
    async with aiomqtt.Client(
        os.environ["SERVIDOR"],
        username=os.environ["MQTT_USR"],
        password=os.environ["MQTT_PASS"],
        port=int(os.environ["PUERTO_MQTTS"]),
>>>>>>> 0a2284b9291a9de08687c1b3f35ad806e392dfa0
        tls_context=tls_context,
    ) as client:
        await client.subscribe(os.environ['TOPICO'])
        async for message in client.messages:
            logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))
            dispositivo=str(message.topic).split('/')[-1]
            datos=json.loads(message.payload.decode('utf8'))
            sql = "INSERT INTO `mediciones` (`sensor_id`, `temperatura`, `humedad`) VALUES (%s, %s, %s)"
            try:
                conn = await aiomysql.connect(host=os.environ["MARIADB_SERVER"], port=3306,
                                            user=os.environ["MARIADB_USER"],
                                            password=os.environ["MARIADB_USER_PASS"],
                                            db=os.environ["MARIADB_DB"])
            except Exception as e:
                logging.error(traceback.format_exc())

            cur = await conn.cursor()

            async with conn.cursor() as cur:
                try:
<<<<<<< HEAD
                    conn = await aiomysql.connect(host=os.environ["MARIADB_SERVER"], port=3306,
                                                user=os.environ["MARIADB_USER"],
                                                password=os.environ["MARIADB_USER_PASS"],
                                                db=os.environ["MARIADB_DB"])
                except Exception as e:
                    logging.error(traceback.format_exc())

                async with conn.cursor() as cur:
                    try:
                        await cur.execute(sql, (message.topic, datos['temperatura'], datos['humedad']))
                        await conn.commit()
                        await cur.close()
                        await conn.ensure_closed()
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        # Logs the error appropriately. 
=======
                    await cur.execute(sql, (dispositivo, datos['temperatura'], datos['humedad']))
                    await conn.commit()
                    await cur.close()
                    await conn.ensure_closed()
                except Exception as e:
                    logging.error(traceback.format_exc())
                    # Logs the error appropriately. 
>>>>>>> 0a2284b9291a9de08687c1b3f35ad806e392dfa0

if __name__ == "__main__":
    asyncio.run(main())