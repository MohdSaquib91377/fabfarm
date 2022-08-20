from rating_review.models import *

def calc_product_avg_rating(product):
    product_rating_total = Rating.objects.filter(product__id = product.id).aggregate(Sum('rating'))['rating__sum']
    if product_rating_total:
        no_of_user_rating_given = Rating.objects.filter(product__id = product.id).count()
        product_rating_avg = product_rating_total / no_of_user_rating_given
        return product_rating_avg
    return None