from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('properties/', views.property_list, name='property_list_alt'),
    path('properties/<int:property_id>/', views.property_detail, name='property_detail'),
    path('cache-metrics/', views.cache_metrics_view, name='cache_metrics'),
]