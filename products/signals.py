from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product
from products.documents.product import ProductDoc


@receiver(post_save, sender=Product)
def my_handler(sender, instance, **kwargs):
    instance.product_indexing()












#
# @receiver(post_save)
# def update_document(sender, **kwargs):
#     """Update document on added/changed records.
#
#     Updates Product document from index if related `product.Unit`
#     (`unit`), `product.Category` (`category`),
#     have been updated from database.
#     """
#     app_label = sender._meta.app_label
#     model_name = sender._meta.model_name
#     instance = kwargs['instance']
#
#     if app_label == 'products':
#         # If it is `product.Category` that is being updated.
#         if model_name == 'category':
#             instances = instance.product.all()
#             for _instance in instances:
#                 registry.update(_instance)
#
#         # If it is `product.Unit` that is being updated.
#         if model_name == 'unit':
#             instances = instance.product.all()
#             for _instance in instances:
#                 registry.update(_instance)
#
#
# @receiver(post_delete)
# def delete_document(sender, **kwargs):
#     """Update document on deleted records.
#
#     Updates Product document from index if related `product.Unit`
#     (`unit`), `product.Category` (`category`),
#     have been removed from database.
#     """
#     app_label = sender._meta.app_label
#     model_name = sender._meta.model_name
#     instance = kwargs['instance']
#
#     if app_label == 'products':
#         # If it is `product.Category` that is being deleted.
#         if model_name == 'category':
#             instances = instance.product.all()
#             for _instance in instances:
#                 registry.update(_instance)
#                 # registry.delete(_instance, raise_on_error=False)
#
#         # If it is `product.Unit` that is being deleted.
#         if model_name == 'unit':
#             instances = instance.product.all()
#             for _instance in instances:
#                 registry.update(_instance)
#                 # registry.delete(_instance, raise_on_error=False)