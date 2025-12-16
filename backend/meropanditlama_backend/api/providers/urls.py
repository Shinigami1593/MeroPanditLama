from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router for viewsets
router = DefaultRouter()
router.register(r'providers', views.ServiceProviderViewSet, basename='provider')
router.register(r'services', views.ServiceViewSet, basename='service')

urlpatterns = [
    # Public routes
    path('', include(router.urls)),
    
    # Provider dashboard routes (provider role only)
    path('provider/dashboard/', views.provider_dashboard, name='provider-dashboard'),
    path('provider/profile/', views.provider_profile, name='provider-profile'),
    path('provider/availability/', views.provider_availability, name='provider-availability'),
    path('provider/availability/<int:slot_id>/', views.provider_availability_detail, name='provider-availability-detail'),
]