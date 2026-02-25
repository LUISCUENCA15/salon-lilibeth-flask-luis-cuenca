from flask import Flask, render_template
from database import init_db, get_inventario

app = Flask(__name__)

# Inicializar base de datos
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

@app.route('/admin/inventario')
def admin_inventario():
    productos = get_inventario()
    return render_template('admin/inventario.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
