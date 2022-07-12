from telnetlib import Telnet
from typing import Text
from unicodedata import category
from store.models import *
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "name": fields.TextField(),
    })

    sub_category = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "name": fields.TextField(),
    })
    brand = fields.ObjectField(properties={
        "id":fields.IntegerField(),
        "name":fields.TextField(),
    })

    images = fields.NestedField(properties={
        "image_caption": fields.TextField(),
        "image": fields.FileField(),
        
    })

    class Index:
        name = "products"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
        
    class Django:
        model = Product
        fields = ["id","name","slug","sku","price","old_price","is_active","is_bestseller","quantity","description","meta_keywords","meta_description"]

    
