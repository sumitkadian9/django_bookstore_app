from store.models import Product
from decimal import Decimal


class Basket():
    """
    provides some default behaviour that can be overrided or inherited
    """

    def __init__(self, request) -> None:
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        add to basket session data
        """
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)}
        
        self.save()

    def update(self, product, qty):
        """
        update product quantity data in session
        """
        product_id = str(product)
        qty = qty

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty

        self.save()

    def remove(self, product):
        """
        delete product from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()
    

    def __len__(self):
        """
        get basket data and count qty of products
        """
        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        """
        query database with ids in session data
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in = product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product
        
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']*item['qty'])
            yield item

    def get_sub_total(self):
        """
        get total price of all products
        """
        return sum((Decimal(item['price'])*item['qty']) for item in self.basket.values())

    def save(self):
        self.session.modified = True