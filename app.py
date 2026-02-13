from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '¡Bienvenido al Salón de Belleza Lilibeth Rodríguez - Reservas y Servicios Premium!'

@app.route('/servicio/<nombre>')
def servicio(nombre):
    return f'¡Bienvenido, {nombre}! Tu cita está confirmada en Lilibeth Rodríguez.'

if __name__ == '__main__':
    app.run(debug=True)
