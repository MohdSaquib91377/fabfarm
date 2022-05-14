
from store.models import *

def is_user_quantity_allowed(product_id,user_selected_quantity):
    if user_selected_quantity < Product.objects.filter(product_id=product_id).first().quantity:
        return True
    return False