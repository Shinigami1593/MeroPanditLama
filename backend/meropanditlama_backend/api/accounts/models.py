from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Custom User model with role-based access."""
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('pandit', 'Pandit'),
        ('lama', 'Lama'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ne', 'Nepali'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^9\d{9}$',
        message="Phone must be 10 digits starting with 9"
    )
    
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(
        validators=[phone_regex],
        max_length=10,
        blank=True,
        help_text="Format: 9841234567"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        db_index=True
    )
    language_pref = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    profile_photo = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email