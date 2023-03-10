from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

# initializations
app = Flask(__name__)

app.config["MYSQL_USER"] = "crud"
app.config["MYSQL_PASSWORD"] = "B(5XsOTjyFPUY.ih"
app.config["MYSQL_DB"] = "agenda"
app.config["MYSQL_HOST"] = "172.19.0.1"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# routes
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

# starting the app
if __name__ == "__main__":
    app.run(port=5000, debug=True,host='0.0.0.0')
