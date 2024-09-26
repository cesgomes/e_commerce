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
        
    def add(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            pass
        else:
            self.cart[product.id] = {'price': str(product.price) }
            
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