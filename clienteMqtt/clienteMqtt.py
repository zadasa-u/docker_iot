import asyncio
import json
import logging
import os
import ssl
import traceback

import aiomysql
import certifi
from asyncio_mqtt import Client, ProtocolVersion

logging.basicConfig(
    format="%(asctime)s - cliente mqtt - %(levelname)s:%(message)s",
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S %z",
)


async def main():
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.minimum_version = ssl.TLSVersion.TLSv1_2
    tls_context.maximum_version = ssl.TLSVersion.TLSv1_3
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

    async with Client(
        os.environ["SERVIDOR"],
        username=os.environ["MQTT_USR"],
        password=os.environ["MQTT_PASS"],
        protocol=ProtocolVersion.V31,
        port=8883,
        tls_context=tls_context,
    ) as client:
        async with client.messages() as messages:
            await client.subscribe("#")
            async for message in messages:
                logging.info(
                    str(message.topic) + ": " + message.payload.decode("utf-8")
                )
                try:
                    conn = await aiomysql.connect(
                        host=os.environ["MARIADB_SERVER"],
                        port=3306,
                        user=os.environ["MARIADB_USER"],
                        password=os.environ["MARIADB_USER_PASS"],
                        db=os.environ["MARIADB_DB"],
                    )
                except Exception as e:
                    logging.error(traceback.format_exc())

                if message.topic.matches("sensores_remotos/#"):
                    datos = json.loads(message.payload.decode("utf8"))
                    sql = "INSERT INTO `mediciones` (`sensor_id`, `temperatura`, `humedad`) VALUES (%s, %s, %s)"
                    async with conn.cursor() as cur:
                        try:
                            await cur.execute(
                                sql,
                                (
                                    str(message.topic).split("/")[1],
                                    datos["temperatura"],
                                    datos["humedad"],
                                ),
                            )
                            await conn.commit()
                            await cur.close()
                            await conn.ensure_closed()
                        except Exception as e:
                            logging.error(traceback.format_exc())
                            # Logs the error appropriately.

                if message.topic.matches("/stackberry/temperatura/+/cpu"):
                    logging.info(
                        str(message.topic).split("/")[3]
                        + ": "
                        + message.payload.decode("utf8")
                    )
                    sql = (
                        "INSERT INTO `temp_cpus` (`cpu`, `temperatura`) VALUES (%s, %s)"
                    )
                    async with conn.cursor() as cur:
                        try:
                            await cur.execute(
                                sql,
                                (
                                    str(message.topic).split("/")[3],
                                    message.payload.decode("utf8"),
                                ),
                            )
                            await conn.commit()
                            await cur.close()
                            await conn.ensure_closed()
                        except Exception as e:
                            logging.error(traceback.format_exc())
                            # Logs the error appropriately.


if __name__ == "__main__":
    asyncio.run(main())
