from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
from .utils import invalidate_property_cache
import logging

logger = logging.getLogger('cache_metrics')


@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, created, **kwargs):
    """
    Signal handler to invalidate property cache when a Property is saved.
    This ensures cache consistency when properties are created or updated.
    """
    action = "created" if created else "updated"
    logger.info(f"Property {action}: {instance.title} (ID: {instance.id})")
    
    # Invalidate the all_properties cache
    invalidate_property_cache()
    
    logger.info(f"Cache invalidated due to property {action}")


@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Signal handler to invalidate property cache when a Property is deleted.
    This ensures cache consistency when properties are removed.
    """
    logger.info(f"Property deleted: {instance.title} (ID: {instance.id})")
    
    # Invalidate the all_properties cache
    invalidate_property_cache()
    
    logger.info("Cache invalidated due to property deletion")