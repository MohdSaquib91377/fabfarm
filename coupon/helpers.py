from coupon.models import Coupon
from django.utils import timezone
from cart.models import Cart
from order.models import *

def validate_coupon(user,coupon_code):
    cart_total,_ = Cart.get_cart_total_item_or_cost(user)  
    print(cart_total)  
    coupon = Coupon.objects.filter(couponCode = coupon_code).first()
    flag = True
    message = coupon

    if not coupon:
        flag = False
        message = "Coupon does not exist"

    elif not coupon.status:
        flag = False
        message = "Invalid Coupon"

    elif not coupon.maxApplyCount > coupon.couponApplyCount: 
        flag = False
        message = "Coupon has been exceed it's maximum quanity"

    elif timezone.now() < coupon.startDateTime:
        flag = False
        message = "Coupon can't be apply before it's offer start"

    elif timezone.now() > coupon.expiryDateTime:
        flag = False
        message = "Coupon has been expired"
    
    elif not cart_total >= coupon.maximumDiscountValue:
        flag = False
        message = f"Coupon will aapply if your order amount max or equal to {coupon.maximumDiscountValue}"
    
    elif not coupon.maxApplyCountPerUser > Order.objects.filter(user = user,coupon = coupon).count():
        flag = False
        message = f"This coupon is only allowed {coupon.maxApplyCountPerUser} times you reach it's max limit"
    return flag, message

def apply_coupon_on_cart_total(user,coupon):
    cart_total,_ = Cart.get_cart_total_item_or_cost(user)  
    if coupon.percentageFlate:
        discount_amount = (cart_total/100)*int(coupon.discountValue)
        total_amount_payble = cart_total - discount_amount
        return cart_total,total_amount_payble,discount_amount,coupon.id
    
    total_amount_payble = cart_total - int(coupon.discountValue)
    return cart_total,total_amount_payble
  