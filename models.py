# ========================================
# 🧱 PRODUCTO (OBLIGATORIO PARA database.py)
# ========================================
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio


# ========================================
# 👤 USER (LOGIN)
# ========================================
from flask_login import UserMixin

# 🔥 IMPORT SEGURO (NO ROMPE SI MYSQL FALLA)
try:
    from conexion.conexion import mysql
except:
    mysql = None


class User(UserMixin):

    def __init__(self, id, nombre, email, password):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

    # ========================================
    # 🔍 BUSCAR POR EMAIL
    # ========================================
    @staticmethod
    def get_by_email(email):
        if not mysql:
            return None

        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM auth_usuarios WHERE email = %s', (email,))
            user_row = cursor.fetchone()
            cursor.close()

            if user_row:
                return User(
                    user_row['id_usuario'],
                    user_row['nombre'],
                    user_row['email'],
                    user_row['password']
                )
            return None

        except Exception as e:
            print(f"ERROR get_by_email: {e}")
            return None

    # ========================================
    # 🔍 BUSCAR POR ID (LOGIN)
    # ========================================
    @staticmethod
    def get(id):
        if not mysql:
            return None

        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM auth_usuarios WHERE id_usuario = %s', (id,))
            user_row = cursor.fetchone()
            cursor.close()

            if user_row:
                return User(
                    user_row['id_usuario'],
                    user_row['nombre'],
                    user_row['email'],
                    user_row['password']
                )
            return None

        except Exception as e:
            print(f"ERROR get: {e}")
            return None

    # ========================================
    # 🆕 CREAR USUARIO
    # ========================================
    @staticmethod
    def create(nombre, email, password):
        if not mysql:
            return False

        try:
            cursor = mysql.connection.cursor()

            cursor.execute('SELECT id_usuario FROM auth_usuarios WHERE email = %s', (email,))
            if cursor.fetchone():
                cursor.close()
                return False

            from werkzeug.security import generate_password_hash
            hashed = generate_password_hash(password)

            cursor.execute(
                'INSERT INTO auth_usuarios (nombre, email, password) VALUES (%s, %s, %s)',
                (nombre, email, hashed)
            )
            mysql.connection.commit()
            cursor.close()

            print("Usuario creado")
            return True

        except Exception as e:
            print(f"ERROR create: {e}")
            return False


# ========================================
# 🔥 DEBUG
# ========================================
class UserModel:

    @staticmethod
    def prueba_total():
        if not mysql:
            print("MySQL no disponible")
            return

        try:
            cursor = mysql.connection.cursor()

            cursor.execute("SELECT DATABASE()")
            print("DB actual:", cursor.fetchone())

            cursor.execute("SELECT COUNT(*) as total FROM auth_usuarios")
            print("TOTAL usuarios:", cursor.fetchone())

            cursor.execute("SELECT * FROM auth_usuarios")
            print("REGISTROS:", cursor.fetchall())

            cursor.close()

        except Exception as e:
            print("ERROR DEBUG:", e)