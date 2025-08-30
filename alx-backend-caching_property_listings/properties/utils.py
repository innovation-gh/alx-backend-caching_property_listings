from django.core.cache import cache
from django.conf import settings
from django_redis import get_redis_connection
from .models import Property
import logging
import time

logger = logging.getLogger('cache_metrics')


def get_all_properties():
    """
    Get all properties with low-level caching.
    Cache the queryset in Redis for 1 hour.
    """
    cache_key = 'all_properties'
    
    # Try to get from cache first
    properties = cache.get(cache_key)
    
    if properties is not None:
        logger.info(f"Cache HIT for key: {cache_key}")
        return properties
    
    # Cache miss - fetch from database
    logger.info(f"Cache MISS for key: {cache_key} - fetching from database")
    
    # Fetch all properties from database
    properties = list(Property.objects.all().order_by('-created_at'))
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set(cache_key, properties, 3600)
    
    logger.info(f"Cached {len(properties)} properties for 1 hour")
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with cache performance statistics.
    """
    try:
        # Get Redis connection
        redis_connection = get_redis_connection("default")
        
        # Get Redis info including keyspace statistics
        redis_info = redis_connection.info()
        
        # Extract hit/miss statistics
        keyspace_hits = int(redis_info.get('keyspace_hits', 0))
        keyspace_misses = int(redis_info.get('keyspace_misses', 0))
        
        # Calculate total requests and hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests * 100) if total_requests > 0 else 0
        
        # Get additional Redis metrics
        used_memory = redis_info.get('used_memory_human', 'N/A')
        connected_clients = redis_info.get('connected_clients', 0)
        total_commands_processed = redis_info.get('total_commands_processed', 0)
        
        # Get cache-specific statistics
        cache_stats = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2),
            'used_memory': used_memory,
            'connected_clients': connected_clients,
            'total_commands_processed': total_commands_processed,
            'timestamp': time.time(),
        }
        
        # Log the metrics
        logger.info(f"Redis Cache Metrics: Hits={keyspace_hits}, Misses={keyspace_misses}, "
                   f"Hit Ratio={hit_ratio:.2f}%, Memory Used={used_memory}")
        
        return cache_stats
        
    except Exception as e:
        logger.error(f"Error fetching Redis cache metrics: {str(e)}")
        return {
            'error': f'Unable to fetch cache metrics: {str(e)}',
            'timestamp': time.time(),
        }


def invalidate_property_cache():
    """
    Helper function to invalidate property-related caches.
    Called by signals when properties are modified.
    """
    cache_keys = [
        'all_properties',
        # Add other related cache keys if needed
    ]
    
    for key in cache_keys:
        cache.delete(key)
        logger.info(f"Invalidated cache key: {key}")


def get_property_cache_info():
    """
    Get information about cached properties
    """
    cache_key = 'all_properties'
    
    # Check if key exists in cache
    cached_data = cache.get(cache_key)
    
    return {
        'cache_key': cache_key,
        'is_cached': cached_data is not None,
        'cached_count': len(cached_data) if cached_data else 0,
        'ttl': cache.ttl(cache_key) if hasattr(cache, 'ttl') else 'N/A',
    }