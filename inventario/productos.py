from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = 'productos_sqlalchemy'
    
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio
        }
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'
