from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_inventario, agregar_producto, eliminar_producto, actualizar_producto, buscar_producto
import os
import json
import csv

# ===== SEMANA 12: SQLAlchemy =====
from inventario.productos import db, Producto as ProductoSQLAlchemy

app = Flask(__name__)

# Configuración SQLAlchemy (Semana 12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon_sqlalchemy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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

# ===== SEMANA 11: CRUD SQLite Anterior =====
@app.route('/admin/inventario', methods=['GET', 'POST'])
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
def admin_eliminar(id_producto):
    eliminar_producto(id_producto)
    return redirect(url_for('admin_inventario'))

@app.route('/admin/buscar/<nombre>')
def admin_buscar(nombre):
    if nombre.strip():
        productos = buscar_producto(nombre)
    else:
        productos = get_inventario()
    return render_template('admin/inventario.html', productos=productos)

# ===== SEMANA 12: PERSISTENCIA TXT/JSON/CSV/SQLAlchemy =====
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


# ===== SEMANA 13: MySQL XAMPP =====
from conexion.conexion import init_mysql, mysql

# Inicializar MySQL
init_mysql(app)

@app.route('/mysql/usuarios')
def mysql_usuarios():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('mysql_usuarios.html', usuarios=usuarios)

@app.route('/productos')
def mostrar_productos():  
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    cursor.close()
    return render_template('mysql_productos.html', productos=productos)

@app.route('/mysql/agregar_usuario', methods=['POST'])
def mysql_agregar_usuario():
    cursor = mysql.connection.cursor()
    nombre = request.form['nombre']
    mail = request.form['mail']
    password = request.form['password']
    cursor.execute('INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)', 
                   (nombre, mail, password))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('mysql_usuarios'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)


