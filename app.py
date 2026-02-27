from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_inventario, agregar_producto, eliminar_producto, actualizar_producto, buscar_producto

app = Flask(__name__)

# Inicializar DB
init_db()

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

if __name__ == '__main__':
    app.run(debug=True)
