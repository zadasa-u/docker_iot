from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging, os, asyncio, aiomysql, traceback, locale, ssl
import matplotlib.pyplot as plt
from io import BytesIO
from aiomqtt import Client

token=os.environ["TB_TOKEN"]

MARIADB_SERVER = os.environ["MARIADB_SERVER"]
MARIADB_USER = os.environ["MARIADB_USER"]
MARIADB_USER_PASS = os.environ["MARIADB_USER_PASS"]
MARIADB_DB = os.environ["MARIADB_DB"]
MARIADB_TABLE = os.environ["MARIADB_TABLE"]

MIN_TEMP = os.environ["MIN_TEMP"]
MAX_TEMP = os.environ["MAX_TEMP"]
OPT_MIN_TEMP = os.environ["OPT_MIN_TEMP"]
OPT_MAX_TEMP = os.environ["OPT_MAX_TEMP"]

# valores predefinidos de intervalo de grafica
intervalo = "DAY"
mod = "2"

logging.basicConfig(format='%(asctime)s - TelegramBot - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("se conectó: " + str(update.message.from_user.id))
    if update.message.from_user.first_name:
        nombre=update.message.from_user.first_name
    else:
        nombre=""
    if update.message.from_user.last_name:
        apellido=update.message.from_user.last_name
    else:
        apellido=""
    kb = [["temperatura"],["humedad"],["gráfico temperatura"],["gráfico humedad"]]
    await context.bot.send_message(
        update.message.chat.id,
        text="Bienvenido al Bot "+ nombre + " " + apellido + ".\n Para informacion acerca de comandos envie /ayuda",
        reply_markup=ReplyKeyboardMarkup(kb)
    )

async def info_ayuda(update: Update, context):
    logging.info(update.message.text)
    info = "Comandos:\n\n\
    /periodo valor: establece el periodo de lectura del sensor al valor proporcionado en segundos.\n\n\
    /intervalo_grafica valor: establece el intervalo de datos de las graficas segun el valor, que puede ser dia, semana o mes.\n\n\
    /ayuda: muestra esta ayuda."
    await context.bot.send_message(
        update.message.chat.id,
        text=info
    )

async def config_grafica(update: Update, context):
    logging.info(update.message.text)
    global intervalo
    global mod
    ok = True

    if context.args:
        valor = context.args[0].lower()
        if valor == "dia":
            intervalo = "DAY"
            mod = 2
        elif valor == "semana":
            intervalo = "WEEK"
            mod = 14
        elif valor == "mes":
            intervalo = "MONTH"
            mod = 56
        else:
            ok = False
    else:
        ok = False
    
    if ok:
        repuesta = "Intervalo ajustado exitosamente"
    else:
        repuesta = "Valor de intervalo incorrecto. Debe ser dia, semana o mes."
    
    await context.bot.send_message(
        update.message.chat.id,
        text=repuesta
    )

async def config_periodo(update: Update, context):
    logging.info(update.message.text)

    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

    if context.args:
        periodo = context.args[0]
        try:
            periodo = int(periodo)
        except:
            repuesta = "Error en el valor"
        
        try:
            async with Client(
                os.environ["SERVIDOR"],
                username=os.environ["MQTT_USR"],
                password=os.environ["MQTT_PASS"],
                port = int(os.environ['PUERTO_MQTTS']),
                tls_context=tls_context,
            ) as client:
                topico = "monitoreo/yatei/periodo"
                logging.info("Publicando en {} el valor: {}".format(topico,periodo))
                await client.publish(topic=topico, payload=periodo, qos=1)

        except OSError as e:
            logging.info(e)
            repuesta = "Error de envio"
        
        repuesta = "Periodo enviado"

    else:
        repuesta = "No hay valor. Debe especificar un valor en segundos"
    
    await context.bot.send_message(
        update.message.chat.id,
        text=repuesta
    )

        
async def medicion(update: Update, context):
    logging.info(update.message.text)
    columna = update.message.text
    
    sql = f"SELECT timestamp, {columna} FROM {MARIADB_TABLE} ORDER BY timestamp DESC LIMIT 1"
    conn = await aiomysql.connect(
        host=MARIADB_SERVER,
        port=3306,
        user=MARIADB_USER,
        password=MARIADB_USER_PASS,
        db=MARIADB_DB
    )
    async with conn.cursor() as cur:
        await cur.execute(sql)
        r = await cur.fetchone()
        if update.message.text == 'temperatura':
            unidad = 'ºC'
        else:
            unidad = '%'
        text = "La última {} es de {} {},\nregistrada a las {:%H:%M:%S %d/%m/%Y}".format(update.message.text, str(r[1]).replace('.',','), unidad, r[0])
        await context.bot.send_message(update.message.chat.id,text=text)
        logging.info(text)
    conn.close()

async def graficos(update: Update, context):
    logging.info(update.message.text)
    global intervalo
    global mod
    columna = update.message.text.split()[1]
    sql = f"SELECT timestamp, {columna} FROM {MARIADB_TABLE} where id mod {mod} = 0 AND timestamp >= NOW() - INTERVAL 1 {intervalo} ORDER BY timestamp"
    conn = await aiomysql.connect(
        host=MARIADB_SERVER,
        port=3306,
        user=MARIADB_USER,
        password=MARIADB_USER_PASS,
        db=MARIADB_DB
    )
    async with conn.cursor() as cur:
        await cur.execute(sql)
        filas = await cur.fetchall()

        fig, ax = plt.subplots(figsize=(7, 4))
        fecha,var=zip(*filas)
        ax.plot(fecha,var,color='k', linewidth=2)
        if columna == "temperatura":
            unidad = 'ºC'
            ax.set_ylim([0,50])
            ax.axhline(y = MIN_TEMP, color = 'r', linestyle = '--', linewidth=1)
            ax.axhline(y = OPT_MIN_TEMP, color = 'y', linestyle = '--', linewidth=1)
            ax.axhline(y = OPT_MAX_TEMP, color = 'y', linestyle = '--', linewidth=1)
            ax.axhline(y = MAX_TEMP, color = 'r', linestyle = '--', linewidth=1)
        else:
            unidad = '%'
            ax.set_ylim([0,100])
        ax.tick_params(axis='x', labelrotation = 45)
        ax.grid(True, which='both')
        ax.set_title(update.message.text, fontsize=14, verticalalignment='bottom')
        ax.set_xlabel('fecha')
        ax.set_ylabel(unidad)

        buffer = BytesIO()
        fig.tight_layout()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buffer)
    conn.close()

def main():
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ayuda', info_ayuda))
    application.add_handler(CommandHandler('intervalo_grafica', config_grafica))
    application.add_handler(CommandHandler('periodo', config_periodo))
    application.add_handler(MessageHandler(filters.Regex("^(temperatura|humedad)$"), medicion))
    application.add_handler(MessageHandler(filters.Regex("^(gráfico temperatura|gráfico humedad)$"), graficos))
    application.run_polling()

if __name__ == '__main__':
    main()
