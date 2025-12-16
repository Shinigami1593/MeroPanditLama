from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from api.accounts.models import User

class Booking(models.Model):
    """Booking model for service requests"""
    
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
        "providers.ServiceProvider",  # <- string reference
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(
        "providers.Service",  # <- string reference
        on_delete=models.SET_NULL,
        null=True,
        related_name='bookings'
    )
    requested_datetime = models.DateTimeField(
        db_index=True,
        help_text="Requested service date and time"
    )
    duration_minutes = models.IntegerField(
        default=60,
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
            models.Index(fields=['requested_datetime', 'status']),
        ]
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user.get_full_name()} → {self.provider.user.get_full_name()}"
    
    @property
    def is_past(self):
        return self.requested_datetime < timezone.now()
    
    @property
    def can_cancel(self):
        return self.status in ['pending', 'confirmed'] and not self.is_past
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_booking = Booking.objects.get(pk=self.pk)
            old_status = old_booking.status
        
        super().save(*args, **kwargs)
        
        from api.providers.models import AvailabilitySlot  # import inside method to avoid circular import
        if self.status == 'confirmed' and old_status != 'confirmed':
            AvailabilitySlot.objects.filter(
                provider=self.provider,
                date=self.requested_datetime.date(),
                start_time__lte=self.requested_datetime.time(),
                end_time__gte=self.requested_datetime.time()
            ).update(is_booked=True)
        elif self.status in ['cancelled', 'completed'] and old_status == 'confirmed':
            AvailabilitySlot.objects.filter(
                provider=self.provider,
                date=self.requested_datetime.date(),
                start_time__lte=self.requested_datetime.time(),
                end_time__gte=self.requested_datetime.time()
            ).update(is_booked=False)
