class Product:
    def __init__(self, uid, name, quantity, price):
        self.uid = uid
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Product(id={self.uid}, name={self.name}, quantity={self.quantity}, price={self.price})"
