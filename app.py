from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import os
import json
import csv

# ===== BASE =====
from database import init_db, get_inventario, agregar_producto, eliminar_producto, buscar_producto

# ===== SQLAlchemy =====
from inventario.productos import db, Producto as ProductoSQLAlchemy

# ===== MySQL =====
try:
    from conexion.conexion import init_mysql, mysql
    MYSQL_AVAILABLE = True
except:
    MYSQL_AVAILABLE = False

# ===== MODELOS =====
from models import User

# ========================================
# APP
# ========================================
app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

# ===== MYSQL =====
if MYSQL_AVAILABLE and not os.environ.get("RENDER"):
    init_mysql(app)
    print("✅ MySQL conectado")

# ===== SQLAlchemy =====
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon_sqlalchemy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ===== LOGIN =====
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# ===== SQLITE =====
init_db()

with app.app_context():
    db.create_all()

# ========================================
# DEBUG DB
# ========================================
@app.route('/debug_db')
def debug_db():
    from models import UserModel
    UserModel.prueba_total()
    return "<h1>Revisa consola</h1>"

# ========================================
# PÚBLICO
# ========================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

# ========================================
# LOGIN
# ========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']

        user = User.get_by_email(email)

        if user:
            print("USUARIO ENCONTRADO")
            print("PASSWORD DB:", user.password)

        if user and check_password_hash(user.password, password):
            login_user(user)
            print("LOGIN OK")
            return redirect(url_for('admin_panel'))

        print("LOGIN FALLÓ")
        return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')

# ========================================
# REGISTER
# ========================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        if User.create(nombre, email, password):
            return redirect(url_for('login'))

        return render_template('register.html', error='Email ya existe')

    return render_template('register.html')

# ========================================
# LOGOUT
# ========================================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ========================================
# PANEL
# ========================================
@app.route('/admin/panel')
@login_required
def admin_panel():
    print("ENTRO AL PANEL")
    return render_template('admin_panel.html', user=current_user)

# ========================================
# INVENTARIO
# ========================================
@app.route('/admin/inventario', methods=['GET', 'POST'])
@login_required
def admin_inventario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        agregar_producto(nombre, cantidad, precio)

    productos = get_inventario()
    return render_template('admin/inventario.html', productos=productos)

# ========================================
# DEBUG MYSQL
# ========================================
@app.route('/debug')
def debug():
    if not MYSQL_AVAILABLE:
        return "MySQL no disponible"

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM auth_usuarios')
    data = cursor.fetchall()
    cursor.close()
    return f"<pre>{data}</pre>"
# ========================================
# MYSQL - USUARIOS
# ========================================
@app.route('/mysql/usuarios')
def mysql_usuarios():
    if not MYSQL_AVAILABLE:
        return "MySQL no disponible"

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM auth_usuarios')
        usuarios = cursor.fetchall()
        cursor.close()
        return render_template('mysql_usuarios.html', usuarios=usuarios)
    except Exception as e:
        return f"Error: {e}"


# ========================================
# MYSQL - PRODUCTOS
# ========================================
@app.route('/productos')
def mysql_productos():
    if not MYSQL_AVAILABLE:
        return "MySQL no disponible"

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        cursor.close()
        return render_template('mysql_productos.html', productos=productos)
    except Exception as e:
        return f"Error: {e}"
    # ========================================
# DATOS (TXT, JSON, CSV, SQLAlchemy)
# ========================================
@app.route('/datos')
def datos():
    return render_template('datos.html',
                           txt_content="Cargando...",
                           json_content="Cargando...",
                           csv_content=[["Cargando..."]],
                           sqlalchemy_productos=[])
@app.route('/datos/txt')
def datos_txt():
    try:
        with open('inventario/data/datos.txt', 'r', encoding='utf-8') as f:
            return render_template('datos.html', txt_content=f.read())
    except:
        return "Error TXT", 500


@app.route('/datos/json')
def datos_json():
    try:
        import json
        with open('inventario/data/datos.json', 'r') as f:
            return render_template('datos.html', json_content=json.dumps(json.load(f), indent=2))
    except:
        return "Error JSON", 500


@app.route('/datos/csv')
def datos_csv():
    try:
        import csv
        with open('inventario/data/datos.csv', 'r') as f:
            return render_template('datos.html', csv_content=list(csv.reader(f)))
    except:
        return "Error CSV", 500


@app.route('/datos/sqlalchemy')
def datos_sqlalchemy():
    productos = ProductoSQLAlchemy.query.all()
    return render_template('datos_sqlalchemy.html', productos=productos)

@app.route('/test')
def test():
    from flask_login import current_user
    return f"Usuario actual: {current_user.is_authenticated}"

# ========================================
# RUN
# ========================================
if __name__ == '__main__':
    app.run(debug=True)