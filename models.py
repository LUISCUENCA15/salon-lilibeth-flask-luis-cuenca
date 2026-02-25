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
