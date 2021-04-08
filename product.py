import json


class ProductsList:
    # doar cele de la search
    def __init__(self):
        self.productsList = []
        self._loadData('products.json')

    def _loadData(self, filename):
        with open(filename) as file:
            self.productsList = json.load(file)

    def getProducts(self):
        return self.productsList

    def getProductById(self, id):
        result = list(filter(lambda x: x["id"] == int(id), self.productsList))
        if len(result) != 0:
            return result[0]
        return None


# not used:
class Product:
    def __init__(self, id, name, price, image):
        self.id = id
        self.name = name
        self.price = price
        self.image = image


class ShoppingCart:
    def __init__(self):
        self.products = []
        self.total = 0

    def addProduct(self, id):
        pass

    def removeProduct(self, id):
        pass

    def getTotal(self):
        pass
