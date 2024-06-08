from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os, logging
from functools import wraps
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash, generate_password_hash

logging.basicConfig(format='%(asctime)s - RSCW - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config["MYSQL_USER"] = os.environ["MYSQL_USER"]
app.config["MYSQL_PASSWORD"] = os.environ["MYSQL_PASSWORD"]
app.config["MYSQL_DB"] = os.environ["MYSQL_DB"]
app.config["MYSQL_HOST"] = os.environ["MYSQL_HOST"]
app.config['PERMANENT_SESSION_LIFETIME']=180
mysql = MySQL(app)

# rutas

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    """Registrar usuario"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("usuario"):
            return "el campo usuario es obligatorio"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "el campo contraseña es obligatorio"

        passhash=generate_password_hash(request.form.get("password"), method='scrypt', salt_length=16)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (usuario, hash) VALUES (%s,%s)", (request.form.get("usuario"), passhash[17:]))
        if mysql.connection.affected_rows():
            flash('Se agregó un usuario')  # usa sesión
            logging.info("se agregó un usuario")
        mysql.connection.commit()
        return redirect(url_for('index'))

    return render_template('registrar.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("usuario"):
            return "el campo usuario es obligatorio"
        # Ensure password was submitted
        elif not request.form.get("password"):
            return "el campo contraseña es obligatorio"

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario LIKE %s", (request.form.get("usuario"),))
        rows=cur.fetchone()

        if(rows):
            if (check_password_hash('scrypt:32768:8:1$' + rows[2],request.form.get("password"))):
                
                session.permanent = True
                
                session["user_id"]=request.form.get("usuario")
                session["tema"] = "claro"

                logging.info("se autenticó correctamente")
                return redirect(url_for('index'))
            else:
                flash('usuario o contraseña incorrecto')
                return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/')
@require_login
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM nodos')
    datos = cur.fetchall()
    cur.close()
    return render_template('index.html', nodos = datos)

@app.route('/add_node', methods=['POST'])
@require_login
def add_node():
    if request.method == 'POST':
        alias = request.form['alias']
        unique_id = request.form['unique_id']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO nodos (alias, unique_id) VALUES (%s,%s)"
                    , (alias, unique_id))
        if mysql.connection.affected_rows():
            flash('Se agregó un nodo')  # usa sesión
            logging.info("se agregó un nodo")
            mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods = ['GET'])
@require_login
def delete_node(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM nodos WHERE id = {0}'.format(id))
    if mysql.connection.affected_rows():
        flash('Se eliminó un nodo')  # usa sesión
        logging.info("se eliminó un nodo")
        mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods = ['GET'])
@require_login
def get_node(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM nodos WHERE id = %s', (id,))
    datos = cur.fetchone()
    logging.info(datos)
    return render_template('editar-nodo.html', nodo = datos)

@app.route('/actualize_node/<id>', methods=['POST'])
@require_login
def actualize_node(id):
    if request.method == 'POST':
        alias = request.form['alias']
        unique_id = request.form['unique_id']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE nodos SET alias=%s, unique_id=%s WHERE id=%s", (alias, unique_id, id))
    if mysql.connection.affected_rows():
        flash('Se actualizó un nodo')  # usa sesión
        logging.info("se actualizó un nodo")
        mysql.connection.commit()
    return redirect(url_for('index'))

@app.route("/logout")
@require_login
def logout():
    session.clear()
    logging.info("el usuario {} cerró su sesión".format(session.get("user_id")))
    return redirect(url_for('index'))

@app.route("/change_theme", methods=['POST'])
@require_login
def change_theme():
    """Alterna entre tema oscuro y claro"""
    if session["tema"] == "claro":
        session["tema"] = "oscuro"
    else:
        session["tema"] = "claro"
    
    logging.info(f'Tema seleccionado: {session["tema"]}')

    return redirect(url_for('index'))
