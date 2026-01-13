from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from api.accounts.models import User

class Booking(models.Model):
    """Booking model for service requests"""
    
    TIME_SLOT_CHOICES = [
        ('morning', 'Morning (8am - 12pm)'),
        ('afternoon', 'Afternoon (12pm - 4pm)'),
        ('evening', 'Evening (4pm - 8pm)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'user'}
    )
    provider = models.ForeignKey(
        "providers.ServiceProvider",
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(
        "providers.Service",
        on_delete=models.SET_NULL,
        null=True,
        related_name='bookings'
    )
    requested_date = models.DateField(
        db_index=True,
        help_text="Requested service date"
    )
    time_slot = models.CharField(
        max_length=10,
        choices=TIME_SLOT_CHOICES,
        default='morning',
        help_text="Preferred time slot"
    )
    duration_minutes = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(30)],
        help_text="Service duration in minutes"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    notes = models.TextField(blank=True, help_text="Additional notes or requirements")
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['provider', 'status']),
            models.Index(fields=['requested_date', 'status']),
        ]
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user.get_full_name()} → {self.provider.user.get_full_name()}"
    
    @property
    def is_past(self):
        """Check if booking date has passed"""
        if self.requested_date is None:
            return False
        return self.requested_date < timezone.now().date()
    
    @property
    def can_cancel(self):
        """Check if booking can be cancelled"""
        if self.requested_date is None:
            return False
        return self.status in ['pending', 'confirmed'] and not self.is_past
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_booking = Booking.objects.get(pk=self.pk)
            old_status = old_booking.status
        
        super().save(*args, **kwargs)
        
        from api.providers.models import AvailabilitySlot
        
        if self.status == 'confirmed' and old_status != 'confirmed':
            # Mark availability slot as booked
            AvailabilitySlot.objects.filter(
                provider=self.provider,
                date=self.requested_date
            ).update(is_booked=True)
        elif self.status in ['cancelled', 'completed'] and old_status == 'confirmed':
            # Mark availability slot as available
            AvailabilitySlot.objects.filter(
                provider=self.provider,
                date=self.requested_date
            ).update(is_booked=False)