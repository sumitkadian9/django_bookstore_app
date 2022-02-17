#functionality for views




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

    def add(self, product):
        """
        add and update basket session data
        """
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {'price': int(product.price)}
        
        self.session.modified = True