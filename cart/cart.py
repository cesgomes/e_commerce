from store.models import Product

class Cart():
    
    def __init__(self, request):
        self.session = request.session
        
        #Get current session key, if exists
        cart = self.session.get('session_key')
        
        # if the user is new, no session key! Create a brand new one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        #Make sure cart is available on all pages of site
        self.cart = cart
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product.id] = {'price': str(product.price) }
            self.cart[product.id] = int(product_qty)
            
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)     
    
    def get_prods(self):

        #get Ids from cart
        product_ids = self.cart.keys()

        #Use ids to lookup itens on database model
        products = Product.objects.filter(id__in=product_ids) 
        
        #Return products found
        return products       
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        #Get Cart
        ourcart = self.cart
        
        #Update Dictionary\Cart
        ourcart[product_id] = product_qty
        
        self.session.modified = True
        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        
    def cart_total(self):
        #Get Product Ids
        product_ids = self.cart.keys()
        #Look up keys in products database
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total += (product.price * value)
        return total