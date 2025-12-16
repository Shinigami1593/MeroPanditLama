from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

from .models import Service, ServiceProvider, AvailabilitySlot, Review
from .serializers import (
    ServiceSerializer, ServiceProviderListSerializer,
    ServiceProviderDetailSerializer, AvailabilitySlotSerializer,
    AvailabilitySlotCreateSerializer, ReviewSerializer,
    ProviderProfileUpdateSerializer
)
from api.accounts.permissions import IsProvider

# PUBLIC ENDPOINTS (No auth required)

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """Public: List all services"""
    
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class ServiceProviderViewSet(viewsets.ReadOnlyModelViewSet):
    """Public: Browse and search providers"""
    
    queryset = ServiceProvider.objects.filter(verified=True).select_related('user')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['religion_type', 'location', 'verified']
    search_fields = ['user__first_name', 'user__last_name', 'location', 'short_description']
    ordering_fields = ['experience_years', 'price_per_service', 'created_at']
    ordering = ['-verified', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceProviderDetailSerializer
        return ServiceProviderListSerializer
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get provider availability for date range"""
        provider = self.get_object()
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if not date_from or not date_to:
            return Response({
                'error': 'date_from and date_to parameters are required (YYYY-MM-DD format)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        slots = AvailabilitySlot.objects.filter(
            provider=provider,
            date__gte=date_from,
            date__lte=date_to
        ).order_by('date', 'start_time')
        
        serializer = AvailabilitySlotSerializer(slots, many=True)
        return Response({
            'provider_id': provider.id,
            'provider_name': provider.user.get_full_name(),
            'date_from': date_from,
            'date_to': date_to,
            'availability': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get provider reviews"""
        provider = self.get_object()
        reviews = Review.objects.filter(provider=provider).select_related('user')
        serializer = ReviewSerializer(reviews, many=True)
        return Response({
            'provider_id': provider.id,
            'average_rating': provider.average_rating,
            'total_reviews': provider.total_reviews,
            'reviews': serializer.data
        })

# PROVIDER DASHBOARD ENDPOINTS (Provider role only)

@api_view(['GET'])
@permission_classes([IsProvider])
def provider_dashboard(request):
    """Provider dashboard with statistics"""
    try:
        provider = request.user.provider_profile
    except ServiceProvider.DoesNotExist:
        return Response({
            'error': 'Provider profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    from api.bookings.models import Booking
    
    # Get statistics
    total_bookings = provider.bookings.count()
    pending_bookings = provider.bookings.filter(status='pending').count()
    confirmed_bookings = provider.bookings.filter(status='confirmed').count()
    completed_bookings = provider.bookings.filter(status='completed').count()
    
    # Recent bookings
    recent_bookings = provider.bookings.order_by('-created_at')[:5]
    from api.bookings.serializers import BookingSerializer
    
    return Response({
        'provider': ServiceProviderDetailSerializer(provider).data,
        'stats': {
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'confirmed_bookings': confirmed_bookings,
            'completed_bookings': completed_bookings,
            'average_rating': provider.average_rating,
            'total_reviews': provider.total_reviews,
        },
        'recent_bookings': BookingSerializer(recent_bookings, many=True).data
    })

@api_view(['GET', 'PUT'])
@permission_classes([IsProvider])
def provider_profile(request):
    """Get or update provider's own profile"""
    try:
        provider = request.user.provider_profile
    except ServiceProvider.DoesNotExist:
        return Response({
            'error': 'Provider profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ServiceProviderDetailSerializer(provider)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProviderProfileUpdateSerializer(
            provider,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'provider': ServiceProviderDetailSerializer(provider).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsProvider])
def provider_availability(request):
    """Get or create availability slots"""
    try:
        provider = request.user.provider_profile
    except ServiceProvider.DoesNotExist:
        return Response({
            'error': 'Provider profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Get provider's availability
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        slots = AvailabilitySlot.objects.filter(provider=provider)
        
        if date_from and date_to:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                slots = slots.filter(date__gte=date_from, date__lte=date_to)
            except ValueError:
                pass
        
        slots = slots.order_by('date', 'start_time')
        serializer = AvailabilitySlotSerializer(slots, many=True)
        return Response({
            'availability': serializer.data
        })
    
    elif request.method == 'POST':
        # Create new availability slot
        serializer = AvailabilitySlotCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(provider=provider)
            return Response({
                'message': 'Availability slot created successfully',
                'slot': AvailabilitySlotSerializer(serializer.instance).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsProvider])
def provider_availability_detail(request, slot_id):
    """Update or delete availability slot"""
    try:
        provider = request.user.provider_profile
    except ServiceProvider.DoesNotExist:
        return Response({
            'error': 'Provider profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    slot = get_object_or_404(AvailabilitySlot, id=slot_id, provider=provider)
    
    if slot.is_booked:
        return Response({
            'error': 'Cannot modify booked slot'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        serializer = AvailabilitySlotCreateSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Availability slot updated successfully',
                'slot': AvailabilitySlotSerializer(serializer.instance).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        slot.delete()
        return Response({
            'message': 'Availability slot deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)