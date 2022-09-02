from rating_review.models import *
from operator import itemgetter

def calc_product_avg_rating(product):
    product_rating_total = Rating.objects.filter(product__id = product.id).aggregate(Sum('rating'))['rating__sum']
    if product_rating_total:
        no_of_user_rating_given = Rating.objects.filter(product__id = product.id).count()
        product_rating_avg = product_rating_total / no_of_user_rating_given
        return product_rating_avg
    return None

def get_sort_by_popularity(products):
    list = []
    dict = {}
    for product in products:
        dict['sum']=0 if product.ratings.filter().aggregate(Sum('rating'))["rating__sum"] is None else product.ratings.filter().aggregate(Sum('rating'))["rating__sum"]
        dict['id']=product.id
        list.append(dict)
        dict = {}
    sorted_list = sorted(list, key=itemgetter('sum'), reverse=True)
    sorted_order_id = []
    for sorted_item in sorted_list:
        sorted_order_id.append(sorted_item['id'])
    return sorted_order_id
