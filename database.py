import sqlite3
from models import Producto

def init_db():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (1, 'keratina', 1, 100.00)")
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (2, 'Tinte', 1, 18.00)")
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (3, 'Tratamientos', 1, 12.00)")
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (4, 'Mascarilla Capilar', 1, 25.00)")
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (5, 'Botox Alisante', 1, 60.00)") 
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (6, 'Planchado de cabello', 1, 30.00)")  
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (7, 'Corte de cabello', 1, 5.00)") 
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (8, 'Listyn de pestañas', 1, 15.00)")
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (9, 'Antifriz', 1, 40.00)")
    cursor.execute("INSERT OR IGNORE INTO productos VALUES (10, 'Reporalizacion', 1, 15.00)")       
    conn.commit()
    conn.close()

def get_inventario():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()
    conn.close()
    return [Producto(*row) for row in rows]

def agregar_producto(nombre, cantidad, precio):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                   (nombre, cantidad, precio))
    conn.commit()
    conn.close()

def eliminar_producto(id_producto):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
    conn.commit()
    conn.close()
