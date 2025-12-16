from rest_framework import serializers
from .models import Service, ServiceProvider, AvailabilitySlot, Review
from api.accounts.serializers import UserSerializer

class ServiceSerializer(serializers.ModelSerializer):
    """Service serializer with language support"""
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'name_ne', 'description', 'description_ne', 'default_price']

class ServiceProviderListSerializer(serializers.ModelSerializer):
    """Serializer for provider list (public view)"""
    
    user = UserSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    total_bookings = serializers.ReadOnlyField()
    
    class Meta:
        model = ServiceProvider
        fields = [
            'id', 'user', 'religion_type', 'experience_years',
            'location', 'short_description', 'short_description_ne',
            'price_per_service', 'services', 'verified',
            'average_rating', 'total_reviews', 'total_bookings'
        ]

class ServiceProviderDetailSerializer(serializers.ModelSerializer):
    """Detailed provider serializer"""
    
    user = UserSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    total_bookings = serializers.ReadOnlyField()
    
    class Meta:
        model = ServiceProvider
        fields = [
            'id', 'user', 'religion_type', 'experience_years',
            'location', 'short_description', 'short_description_ne',
            'price_per_service', 'services', 'verified',
            'created_at', 'average_rating', 'total_reviews', 'total_bookings'
        ]

class AvailabilitySlotSerializer(serializers.ModelSerializer):
    """Availability slot serializer"""
    
    class Meta:
        model = AvailabilitySlot
        fields = ['id', 'date', 'start_time', 'end_time', 'is_booked', 'notes']
        read_only_fields = ['is_booked']
    
    def validate(self, attrs):
        """Validate time slot"""
        if attrs['end_time'] <= attrs['start_time']:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time'
            })
        return attrs

class AvailabilitySlotCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating availability slots"""
    
    class Meta:
        model = AvailabilitySlot
        fields = ['date', 'start_time', 'end_time', 'notes']
    
    def create(self, validated_data):
        # Provider is set from request.user in the view
        return AvailabilitySlot.objects.create(**validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class ProviderProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for provider updating their own profile"""
    
    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all(),
        required=False
    )
    
    class Meta:
        model = ServiceProvider
        fields = [
            'experience_years', 'location', 'short_description',
            'short_description_ne', 'price_per_service', 'services'
        ]