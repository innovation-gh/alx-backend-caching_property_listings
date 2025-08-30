from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Admin configuration for Property model
    """
    list_display = ('title', 'formatted_price', 'location', 'created_at', 'is_expensive')
    list_filter = ('location', 'created_at', 'price')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Financial Information', {
            'fields': ('price',),
            'classes': ('collapse',)
        }),
        ('Location & Metadata', {
            'fields': ('location', 'created_at')
        }),
    )