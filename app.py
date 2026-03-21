from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import init_db, get_inventario, agregar_producto, eliminar_producto, actualizar_producto, buscar_producto
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import csv

# ===== SEMANA 12: SQLAlchemy =====
from inventario.productos import db, Producto as ProductoSQLAlchemy

app = Flask(__name__)
app.secret_key = 'salon-lilibeth-super-secreto-2026'  # ← OBLIGATORIO

# Configuración SQLAlchemy (Semana 12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon_sqlalchemy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ===== FLASK-LOGIN INICIALIZADO PRIMERO =====
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión'

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# Inicializar DB SQLite anterior (Semana 11)
init_db()

# Crear tablas SQLAlchemy (Semana 12)
with app.app_context():
    db.create_all()
    
    # Datos de ejemplo SQLAlchemy
    if not ProductoSQLAlchemy.query.first():
        productos_ejemplo = [
            ProductoSQLAlchemy(nombre='Keratina', cantidad=1, precio=100.00),
            ProductoSQLAlchemy(nombre='Tinte Rubio', cantidad=1, precio=18.00),
            ProductoSQLAlchemy(nombre='Botox Alisante', cantidad=1, precio=60.00)
        ]
        for prod in productos_ejemplo:
            db.session.add(prod)
        db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/servicio/<nombre>')
def servicio(nombre):
    return render_template('servicios.html', nombre=nombre)

# ===== SEMANA 14: LOGIN (CORREGIDO) =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin_panel'))
        return render_template('login.html', error='Email o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        if User.create(nombre, email, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Email ya registrado')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin/panel')
@login_required
def admin_panel():
    return render_template('admin_panel.html', user=current_user)

# ===== SEMANA 11: CRUD SQLite (PROTEGIDO) =====
@app.route('/admin/inventario', methods=['GET', 'POST'])
@login_required
def admin_inventario():
    if request.method == 'POST':
        accion = request.form['accion']
        if accion == 'añadir':
            nombre = request.form['nombre']
            cantidad = int(request.form['cantidad'])
            precio = float(request.form['precio'])
            agregar_producto(nombre, cantidad, precio)
            return redirect(url_for('admin_inventario'))
    
    productos = get_inventario()
    return render_template('admin/inventario.html', productos=productos)

@app.route('/admin/eliminar/<int:id_producto>')
@login_required
def admin_eliminar(id_producto):
    eliminar_producto(id_producto)
    return redirect(url_for('admin_inventario'))

@app.route('/admin/buscar/<nombre>')
@login_required
def admin_buscar(nombre):
    if nombre.strip():
        productos = buscar_producto(nombre)
    else:
        productos = get_inventario()
    return render_template('admin/inventario.html', productos=productos)

# ===== SEMANA 12: PERSISTENCIA =====
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
            content = f.read()
        return render_template('datos.html', txt_content=content)
    except:
        return "Error TXT", 500

@app.route('/datos/json')
def datos_json():
    try:
        import json
        with open('inventario/data/datos.json', 'r') as f:
            data = json.load(f)
        return render_template('datos.html', json_content=json.dumps(data, indent=2))
    except:
        return "Error JSON", 500

@app.route('/datos/csv')
def datos_csv():
    try:
        import csv
        with open('inventario/data/datos.csv', 'r') as f:
            reader = csv.reader(f)
            content = list(reader)
        return render_template('datos.html', csv_content=content)
    except:
        return "Error CSV", 500

@app.route('/datos/sqlalchemy')
def datos_sqlalchemy():
    productos = ProductoSQLAlchemy.query.all()
    return render_template('datos_sqlalchemy.html', productos=productos)

# ===== SEMANA 13: MySQL =====
try:
    from conexion.conexion import init_mysql, mysql
    MYSQL_AVAILABLE = True
    init_mysql(app)
except:
    MYSQL_AVAILABLE = False

def is_local():
    return not os.environ.get('PORT')

@app.route('/mysql/usuarios')
def mysql_usuarios():
    try:
        if is_local() and MYSQL_AVAILABLE:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM auth_usuarios')
            usuarios = cursor.fetchall()
            cursor.close()
            return render_template('mysql_usuarios.html', usuarios=usuarios)
    except:
        pass
    return render_template('mysql_info.html', tipo="usuarios")

@app.route('/productos')
def mostrar_productos():
    try:
        if is_local() and MYSQL_AVAILABLE:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM productos')
            productos = cursor.fetchall()
            cursor.close()
            return render_template('mysql_productos.html', productos=productos)
    except:
        pass
    return render_template('mysql_info.html', tipo="productos")

@app.route('/mysql/agregar_usuario', methods=['POST'])
def mysql_agregar_usuario():
    try:
        if is_local() and MYSQL_AVAILABLE:
            cursor = mysql.connection.cursor()
            nombre = request.form['nombre']
            mail = request.form['mail']
            password = request.form['password']
            cursor.execute('INSERT INTO auth_usuarios (nombre, email, password) VALUES (%s, %s, %s)', 
                          (nombre, mail, password))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('mysql_usuarios'))
    except:
        pass
    return redirect(url_for('mysql_usuarios'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)