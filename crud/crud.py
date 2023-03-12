from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

app.config["MYSQL_USER"] = os.environ["MYSQL_USER"]
app.config["MYSQL_PASSWORD"] = os.environ["MYSQL_PASSWORD"]
app.config["MYSQL_DB"] = os.environ["MYSQL_DB"]
app.config["MYSQL_HOST"] = os.environ["MYSQL_HOST"]
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# rutas
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    datos = cur.fetchall()
    cur.close()
    return render_template('index.html', contactos = datos)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tel = request.form['tel']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contactos (nombre, tel, email) VALUES (%s,%s,%s)"
                    , (nombre, tel, email))
        mysql.connection.commit()
        return redirect(url_for('index'))
