from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.accounts.models import User

class Service(models.Model):
    """Services offered by providers (Puja, Bartabanda, etc.)"""
    
    name = models.CharField(max_length=100, unique=True)
    name_ne = models.CharField(max_length=100, blank=True, verbose_name="Name (Nepali)")
    description = models.TextField(blank=True)
    description_ne = models.TextField(blank=True, verbose_name="Description (Nepali)")
    default_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Default price in NPR"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'services'
        ordering = ['name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    """Provider profile for Pandits and Lamas"""
    
    RELIGION_CHOICES = [
        ('hindu', 'Hindu Pandit'),
        ('buddhist', 'Buddhist Lama'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='provider_profile',
        limit_choices_to={'role': 'provider'}
    )
    religion_type = models.CharField(
        max_length=10,
        choices=RELIGION_CHOICES,
        db_index=True
    )
    experience_years = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Years of experience"
    )
    location = models.CharField(
        max_length=200,
        db_index=True,
        help_text="Primary service location"
    )
    short_description = models.TextField(
        max_length=500,
        help_text="Brief description (English)"
    )
    short_description_ne = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Short Description (Nepali)"
    )
    price_per_service = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Base price per service in NPR"
    )
    services = models.ManyToManyField(
        Service,
        related_name='providers',
        blank=True
    )
    verified = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Admin verified provider"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_providers'
        ordering = ['-verified', '-created_at']
        verbose_name = 'Service Provider'
        verbose_name_plural = 'Service Providers'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_religion_type_display()}"
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        from django.db.models import Avg
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else None
    
    @property
    def total_reviews(self):
        """Get total number of reviews"""
        return self.reviews.count()
    
    @property
    def total_bookings(self):
        """Get total completed bookings"""
        return self.bookings.filter(status='completed').count()

class AvailabilitySlot(models.Model):
    """Provider availability time slots"""
    
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='availability_slots'
    )
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Automatically set when booking confirmed"
    )
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'availability_slots'
        ordering = ['date', 'start_time']
        unique_together = [['provider', 'date', 'start_time']]
        verbose_name = 'Availability Slot'
        verbose_name_plural = 'Availability Slots'
    
    def __str__(self):
        return f"{self.provider.user.get_full_name()} - {self.date} {self.start_time}-{self.end_time}"
    
    def clean(self):
        """Validate that end_time is after start_time"""
        from django.core.exceptions import ValidationError
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time')

class Review(models.Model):
    """User reviews for providers"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    booking = models.OneToOneField(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='review',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        return f"{self.user.get_full_name()} -> {self.provider.user.get_full_name()} ({self.rating}★)"