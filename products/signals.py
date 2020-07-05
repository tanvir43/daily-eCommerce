from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.apps import registry

@receiver(post_save)
def update_document(sender, **kwargs):
    """Update document on added/changed records.

    Updates Product document from index if related `product.Unit`
    (`unit`), `product.Category` (`category`),
    have been updated from database.
    """
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'products':
        # If it is `product.Category` that is being updated.
        if model_name == 'category':
            instances = instance.product.all()
            for _instance in instances:
                registry.update(_instance)

        # If it is `product.Unit` that is being updated.
        if model_name == 'unit':
            instances = instance.product.all()
            for _instance in instances:
                registry.update(_instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    """Update document on deleted records.

    Updates Product document from index if related `product.Unit`
    (`unit`), `product.Category` (`category`),
    have been removed from database.
    """
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'products':
        # If it is `product.Category` that is being updated.
        if model_name == 'category':
            instances = instance.product.all()
            for _instance in instances:
                registry.update(_instance)
                # registry.delete(_instance, raise_on_error=False)

        # If it is `product.Unit` that is being updated.
        if model_name == 'unit':
            instances = instance.product.all()
            for _instance in instances:
                registry.update(_instance)
                # registry.delete(_instance, raise_on_error=False)