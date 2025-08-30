from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics
import logging

logger = logging.getLogger(__name__)


@cache_page(60 * 15)  # Cache for 15 minutes
@require_http_methods(["GET"])
def property_list(request):
    """
    View to list all properties with caching applied at view level
    """
    try:
        # Use the cached queryset function
        properties = get_all_properties()
        
        # Pagination
        paginator = Paginator(properties, 10)  # Show 10 properties per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Return JSON response for API usage
        if request.headers.get('Accept') == 'application/json':
            properties_data = []
            for prop in page_obj:
                properties_data.append({
                    'id': prop.id,
                    'title': prop.title,
                    'description': prop.description,
                    'price': str(prop.price),
                    'formatted_price': prop.formatted_price(),
                    'location': prop.location,
                    'created_at': prop.created_at.isoformat(),
                    'is_expensive': prop.is_expensive,
                })
            
            return JsonResponse({
                'properties': properties_data,
                'total_count': paginator.count,
                'page_count': paginator.num_pages,
                'current_page': page_obj.number,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            })
        
        # Render HTML template
        context = {
            'properties': page_obj,
            'total_properties': paginator.count,
        }
        return render(request, 'properties/property_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in property_list view: {str(e)}")
        return JsonResponse({'error': 'Unable to fetch properties'}, status=500)


def cache_metrics_view(request):
    """
    View to display Redis cache metrics
    """
    try:
        metrics = get_redis_cache_metrics()
        return JsonResponse(metrics)
    except Exception as e:
        logger.error(f"Error fetching cache metrics: {str(e)}")
        return JsonResponse({'error': 'Unable to fetch cache metrics'}, status=500)


@require_http_methods(["GET"])
def property_detail(request, property_id):
    """
    View to get a single property by ID
    """
    try:
        property_obj = Property.objects.get(id=property_id)
        
        property_data = {
            'id': property_obj.id,
            'title': property_obj.title,
            'description': property_obj.description,
            'price': str(property_obj.price),
            'formatted_price': property_obj.formatted_price(),
            'location': property_obj.location,
            'created_at': property_obj.created_at.isoformat(),
            'is_expensive': property_obj.is_expensive,
        }
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'property': property_data})
        
        context = {'property': property_obj}
        return render(request, 'properties/property_detail.html', context)
        
    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in property_detail view: {str(e)}")
        return JsonResponse({'error': 'Unable to fetch property'}, status=500)