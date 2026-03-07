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
            ProductoSQLAlchemy(nombre='Keratina Premium', cantidad=5, precio=100.00),
            ProductoSQLAlchemy(nombre='Tinte Rubio', cantidad=10, precio=18.00),
            ProductoSQLAlchemy(nombre='Botox Alisante', cantidad=3, precio=60.00)
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
    except Exception as e:
        return render_template('datos.html', txt_content=f"Error TXT: {str(e)}")

@app.route('/datos/json')
def datos_json():
    try:
        # Crear JSON si no existe
        if not os.path.exists('inventario/data/datos.json'):
            datos = [
                {'id_producto': 1, 'nombre': 'Keratina', 'cantidad': 1, 'precio': 100.00},
                {'id_producto': 2, 'nombre': 'Tinte', 'cantidad': 1, 'precio': 18.00}
            ]
            with open('inventario/data/datos.json', 'w') as f:
                json.dump(datos, f, indent=2)
        
        with open('inventario/data/datos.json', 'r') as f:
            data = json.load(f)
        return render_template('datos.html', json_content=json.dumps(data, indent=2))
    except Exception as e:
        return render_template('datos.html', json_content=f"Error JSON: {str(e)}")

@app.route('/datos/csv')
def datos_csv():
    try:
        # Crear CSV si no existe
        if os.path.getsize('inventario/data/datos.csv') == 0:
            with open('inventario/data/datos.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'nombre', 'cantidad', 'precio'])
                writer.writerow([1, 'Keratina', 1, 100.00])
                writer.writerow([2, 'Tinte', 1, 18.00])
        
        with open('inventario/data/datos.csv', 'r') as f:
            reader = csv.reader(f)
            content = list(reader)
        return render_template('datos.html', csv_content=content)
    except Exception as e:
        return render_template('datos.html', csv_content=[[f"Error CSV: {str(e)}"]])

@app.route('/datos/sqlalchemy')
def datos_sqlalchemy():
    try:
        productos = ProductoSQLAlchemy.query.all()
        return render_template('datos.html', sqlalchemy_productos=productos)
    except Exception as e:
        return render_template('datos.html', sqlalchemy_productos=[], 
                             txt_content=f"Error SQLAlchemy: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


