from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

from .models import Booking
from api.providers.models import ServiceProvider, Service
from api.providers.serializers import ServiceSerializer
from api.accounts.serializers import UserSerializer

class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings"""
    
    provider_id = serializers.IntegerField(write_only=True)
    service_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'provider_id', 'service_id', 'requested_datetime',
            'duration_minutes', 'notes'
        ]
    
    def validate_provider_id(self, value):
        """Validate provider exists and is verified"""
        try:
            provider = ServiceProvider.objects.get(id=value, verified=True)
        except ServiceProvider.DoesNotExist:
            raise serializers.ValidationError("Provider not found or not verified")
        return value
    
    def validate_service_id(self, value):
        """Validate service exists"""
        try:
            Service.objects.get(id=value)
        except Service.DoesNotExist:
            raise serializers.ValidationError("Service not found")
        return value
    
    def validate_requested_datetime(self, value):
        """Validate booking is at least 24 hours in advance"""
        if value < timezone.now() + timedelta(hours=24):
            raise serializers.ValidationError(
                "Bookings must be made at least 24 hours in advance"
            )
        return value
    
    def validate(self, attrs):
        """Check for booking conflicts"""
        provider = ServiceProvider.objects.get(id=attrs['provider_id'])
        requested_dt = attrs['requested_datetime']
        duration = attrs['duration_minutes']
        end_dt = requested_dt + timedelta(minutes=duration)
        
        # Check for conflicting bookings
        conflicts = Booking.objects.filter(
            provider=provider,
            status__in=['pending', 'confirmed']
        ).filter(
            Q(requested_datetime__lt=end_dt) &
            Q(requested_datetime__gte=requested_dt - timedelta(minutes=60))
        )
        
        if conflicts.exists():
            raise serializers.ValidationError({
                'requested_datetime': 'This time slot is not available. Please choose another time.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create booking"""
        provider = ServiceProvider.objects.get(id=validated_data.pop('provider_id'))
        service = Service.objects.get(id=validated_data.pop('service_id'))
        user = self.context['request'].user
        
        booking = Booking.objects.create(
            user=user,
            provider=provider,
            service=service,
            **validated_data
        )
        
        # Send email notification to provider
        from api.notifications.utils import send_booking_notification
        send_booking_notification(booking, 'requested', provider.user)
        
        return booking

class BookingSerializer(serializers.ModelSerializer):
    """Complete booking serializer"""
    
    user = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    provider_name = serializers.SerializerMethodField()
    provider_phone = serializers.SerializerMethodField()
    provider_religion = serializers.CharField(source='provider.religion_type', read_only=True)
    can_cancel = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'provider_name', 'provider_phone', 'provider_religion',
            'service', 'requested_datetime', 'duration_minutes',
            'status', 'notes', 'cancellation_reason',
            'can_cancel', 'created_at', 'updated_at'
        ]
    
    def get_provider_name(self, obj):
        return obj.provider.user.get_full_name()
    
    def get_provider_phone(self, obj):
        return obj.provider.user.phone

class BookingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing bookings"""
    
    provider_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source='service.name', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user_name', 'provider_name', 'service_name',
            'requested_datetime', 'duration_minutes', 'status', 'created_at'
        ]
    
    def get_provider_name(self, obj):
        return obj.provider.user.get_full_name()
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()

class BookingCancelSerializer(serializers.Serializer):
    """Serializer for cancelling bookings"""
    
    cancellation_reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500
    )