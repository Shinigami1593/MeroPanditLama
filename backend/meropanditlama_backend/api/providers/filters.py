import django_filters
from .models import ServiceProvider

class ServiceProviderFilter(django_filters.FilterSet):
    """Advanced filtering for providers"""
    
    min_experience = django_filters.NumberFilter(
        field_name='experience_years',
        lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='price_per_service',
        lookup_expr='lte'
    )
    service = django_filters.NumberFilter(
        field_name='services',
        lookup_expr='exact'
    )
    
    class Meta:
        model = ServiceProvider
        fields = ['religion_type', 'location', 'verified']