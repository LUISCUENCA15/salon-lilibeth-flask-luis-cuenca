# TU CÓDIGO EXISTENTE (NO CAMBIAR)
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
    
    def to_dict(self):
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio
        }
    
    def __str__(self):
        return f"{self.nombre} (x{self.cantidad}) - ${self.precio}"

class Inventario:
    def __init__(self):
        self.productos = {}
    
    def agregar(self, producto):
        self.productos[producto.id_producto] = producto
    
    def eliminar(self, id_producto):
        return self.productos.pop(id_producto, None)
    
    def actualizar(self, id_producto, cantidad=None, precio=None):
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].cantidad = cantidad
            if precio is not None:
                self.productos[id_producto].precio = precio
            return True
        return False
    
    def buscar(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
    
    def todos(self):
        return list(self.productos.values())

# ===== SEMANA 14: FLASK-LOGIN con auth_usuarios =====
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from conexion.conexion import mysql

class User(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM auth_usuarios WHERE id_usuario = %s', (user_id,))
            user_row = cursor.fetchone()
            cursor.close()
            if user_row:
                return User(user_row[0], user_row[1], user_row[2], user_row[3])
            return None
        except:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM auth_usuarios WHERE email = %s', (email,))
            user_row = cursor.fetchone()
            cursor.close()
            if user_row:
                return User(user_row[0], user_row[1], user_row[2], user_row[3])
            return None
        except:
            return None

    @staticmethod
    def create(nombre, email, password):
        try:
            hashed_password = generate_password_hash(password)
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO auth_usuarios (nombre, email, password) VALUES (%s, %s, %s)', 
                          (nombre, email, hashed_password))
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False