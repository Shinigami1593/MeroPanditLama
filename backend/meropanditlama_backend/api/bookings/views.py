from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Booking
from .serializers import (
    BookingSerializer, BookingListSerializer,
    BookingCreateSerializer, BookingCancelSerializer
)

class BookingViewSet(viewsets.ModelViewSet):
    """Booking management endpoints"""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        """Return bookings based on user role"""
        user = self.request.user
        
        if user.role == 'provider':
            # Provider sees bookings for their services
            return Booking.objects.filter(
                provider__user=user
            ).select_related('user', 'provider__user', 'service').order_by('-created_at')
        else:
            # Regular user sees their own bookings
            return Booking.objects.filter(
                user=user
            ).select_related('user', 'provider__user', 'service').order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        elif self.action == 'list':
            return BookingSerializer
        return BookingSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new booking (User only)"""
        if request.user.role != 'user':
            return Response({
                'error': 'Only users can create bookings'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            booking = serializer.save()
            # Refresh to get related objects
            booking = Booking.objects.select_related('user', 'provider__user', 'service').get(pk=booking.pk)
            return Response({
                'message': 'Booking request sent successfully',
                'booking': BookingSerializer(booking).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking (Provider only)"""
        booking = self.get_object()
        
        # Check if provider owns this booking
        if booking.provider.user != request.user:
            return Response({
                'error': 'You can only confirm your own bookings'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status != 'pending':
            return Response({
                'error': f'Cannot confirm booking with status: {booking.status}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'confirmed'
        booking.save()
        
        return Response({
            'message': 'Booking confirmed successfully',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a booking (Provider only)"""
        booking = self.get_object()
        
        if booking.provider.user != request.user:
            return Response({
                'error': 'You can only reject your own bookings'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status != 'pending':
            return Response({
                'error': f'Cannot reject booking with status: {booking.status}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'cancelled'
        booking.cancellation_reason = request.data.get('reason', 'Rejected by provider')
        booking.save()
        
        return Response({
            'message': 'Booking rejected',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking (User or Provider)"""
        booking = self.get_object()
        
        # Check authorization
        if booking.user != request.user and booking.provider.user != request.user:
            return Response({
                'error': 'Not authorized to cancel this booking'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if not booking.can_cancel:
            return Response({
                'error': 'This booking cannot be cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookingCancelSerializer(data=request.data)
        if serializer.is_valid():
            booking.status = 'cancelled'
            booking.cancellation_reason = serializer.validated_data.get(
                'cancellation_reason',
                f'Cancelled by {request.user.get_full_name()}'
            )
            booking.save()
            
            return Response({
                'message': 'Booking cancelled successfully',
                'booking': BookingSerializer(booking).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark booking as completed (Provider only)"""
        booking = self.get_object()
        
        if booking.provider.user != request.user:
            return Response({
                'error': 'You can only complete your own bookings'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status != 'confirmed':
            return Response({
                'error': 'Only confirmed bookings can be marked as completed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'completed'
        booking.save()
        
        return Response({
            'message': 'Booking marked as completed',
            'booking': BookingSerializer(booking).data
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_history(request):
    """Get booking history organized by status"""
    user = request.user
    
    if user.role == 'provider':
        bookings = Booking.objects.filter(provider__user=user).select_related('user', 'provider__user', 'service')
    else:
        bookings = Booking.objects.filter(user=user).select_related('user', 'provider__user', 'service')
    
    upcoming = bookings.filter(
        status__in=['pending', 'confirmed']
    ).order_by('requested_date')[:10]
    
    completed = bookings.filter(
        status='completed'
    ).order_by('-requested_date')[:10]
    
    cancelled = bookings.filter(
        status='cancelled'
    ).order_by('-updated_at')[:10]
    
    return Response({
        'upcoming': BookingSerializer(upcoming, many=True).data,
        'completed': BookingSerializer(completed, many=True).data,
        'cancelled': BookingSerializer(cancelled, many=True).data
    })