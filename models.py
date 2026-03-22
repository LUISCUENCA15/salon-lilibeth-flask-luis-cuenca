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
class User:

    def __init__(self, id, nombre, email, password):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

    # 🔐 Flask-Login
    def is_authenticated(self): return True
    def is_active(self): return True
    def is_anonymous(self): return False
    def get_id(self): return str(self.id)

    # ========================================
    # 🔍 MÉTODOS MYSQL
    # ========================================

    @staticmethod
    def test_connection():
        try:
            from conexion.conexion import mysql
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT COUNT(*) as total FROM auth_usuarios')
            result = cursor.fetchone()
            count = result['total'] if result else 0
            cursor.close()
            print(f"🧪 TEST OK: {count} usuarios")
            return count
        except Exception as e:
            print(f"🧪 ERROR: {e}")
            return 0

    @staticmethod
    def get_by_email(email):
        print(f"🔍 Buscando: {email}")
        try:
            from conexion.conexion import mysql
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM auth_usuarios WHERE email = %s', (email,))
            user_row = cursor.fetchone()
            cursor.close()

            print("📊 Resultado:", user_row)

            if user_row:
                return User(
                    user_row['id_usuario'],
                    user_row['nombre'],
                    user_row['email'],
                    user_row['password']
                )
            return None

        except Exception as e:
            print(f"❌ ERROR get_by_email: {e}")
            return None

    @staticmethod
    def get(id):
        try:
            from conexion.conexion import mysql
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM auth_usuarios WHERE id = %s', (id,))
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
            print(f"❌ ERROR get: {e}")
            return None

    @staticmethod
    def create(nombre, email, password):
        try:
            from conexion.conexion import mysql
            cursor = mysql.connection.cursor()

            # Verificar si ya existe
            cursor.execute('SELECT id FROM auth_usuarios WHERE email = %s', (email,))
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

            print("✅ Usuario creado")
            return True

        except Exception as e:
            print(f"❌ ERROR create: {e}")
            return False


# ========================================
# 🔥 DEBUG (MUY IMPORTANTE)
# ========================================
class UserModel:

    @staticmethod
    def prueba_total():
        try:
            from conexion.conexion import mysql
            cursor = mysql.connection.cursor()

            cursor.execute("SELECT DATABASE()")
            print("📌 DB actual:", cursor.fetchone())

            cursor.execute("SELECT COUNT(*) as total FROM auth_usuarios")
            print("📊 TOTAL usuarios:", cursor.fetchone())

            cursor.execute("SELECT * FROM auth_usuarios")
            print("📋 REGISTROS:", cursor.fetchall())

            cursor.close()

        except Exception as e:
            print("❌ ERROR DEBUG:", e)