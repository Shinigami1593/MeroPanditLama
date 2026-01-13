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
    
    class Meta:
        model = Booking
        fields = [
            'provider', 'service', 'requested_date',
            'time_slot', 'duration_minutes', 'notes'
        ]
    
    def validate_provider(self, value):
        """Validate provider exists and is verified"""
        if not value.verified:
            raise serializers.ValidationError("Provider is not verified")
        return value
    
    def validate_requested_date(self, value):
        """Validate booking is for a future date"""
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "Booking date must be in the future"
            )
        return value
    
    def validate(self, attrs):
        """Check for booking conflicts"""
        provider = attrs['provider']
        requested_date = attrs['requested_date']
        time_slot = attrs['time_slot']
        
        # Check for conflicting bookings on same date and time slot
        conflicts = Booking.objects.filter(
            provider=provider,
            requested_date=requested_date,
            time_slot=time_slot,
            status__in=['pending', 'confirmed']
        )
        
        if conflicts.exists():
            raise serializers.ValidationError({
                'time_slot': 'This time slot is already booked. Please choose another time.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create booking"""
        user = self.context['request'].user
        
        booking = Booking.objects.create(
            user=user,
            **validated_data
        )
        
        return booking

class BookingSerializer(serializers.ModelSerializer):
    """Complete booking serializer"""
    
    user = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    provider_name = serializers.SerializerMethodField()
    provider_phone = serializers.SerializerMethodField()
    provider_photo = serializers.SerializerMethodField()
    provider_religion = serializers.CharField(source='provider.religion_type', read_only=True)
    can_cancel = serializers.ReadOnlyField()
    time_slot_display = serializers.CharField(source='get_time_slot_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'provider_name', 'provider_phone', 'provider_photo',
            'provider_religion', 'service', 'requested_date', 'time_slot', 
            'time_slot_display', 'duration_minutes', 'status', 'notes', 
            'cancellation_reason', 'can_cancel', 'created_at', 'updated_at'
        ]
    
    def get_provider_name(self, obj):
        return obj.provider.user.get_full_name()
    
    def get_provider_phone(self, obj):
        return obj.provider.user.phone
    
    def get_provider_photo(self, obj):
        """Get provider's profile photo"""
        if obj.provider.user.profile_photo:
            return obj.provider.user.profile_photo.url
        return None

class BookingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing bookings"""
    
    provider_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source='service.name', read_only=True)
    user_name = serializers.SerializerMethodField()
    time_slot_display = serializers.CharField(source='get_time_slot_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user_name', 'provider_name', 'service_name',
            'requested_date', 'time_slot', 'time_slot_display',
            'duration_minutes', 'status', 'created_at'
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