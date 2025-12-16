from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'get_user_name', 'get_provider_name',
        'get_service_name', 'requested_datetime',
        'status_badge', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'requested_datetime']
    search_fields = [
        'user__first_name', 'user__last_name', 'user__email',
        'provider__user__first_name', 'provider__user__last_name',
        'service__name'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'can_cancel', 'is_past'
    ]
    date_hierarchy = 'requested_datetime'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Booking Information', {
            'fields': (
                'user', 'provider', 'service',
                'requested_datetime', 'duration_minutes'
            )
        }),
        ('Status', {
            'fields': ('status', 'notes', 'cancellation_reason')
        }),
        ('Metadata', {
            'fields': ('can_cancel', 'is_past', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    get_user_name.short_description = 'User'
    get_user_name.admin_order_field = 'user__first_name'
    
    def get_provider_name(self, obj):
        return obj.provider.user.get_full_name()
    get_provider_name.short_description = 'Provider'
    get_provider_name.admin_order_field = 'provider__user__first_name'
    
    def get_service_name(self, obj):
        return obj.service.name if obj.service else '-'
    get_service_name.short_description = 'Service'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'completed': '#17a2b8',
            'cancelled': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} booking(s) marked as confirmed.')
    mark_confirmed.short_description = 'Mark as Confirmed'
    
    def mark_completed(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='completed')
        self.message_user(request, f'{updated} booking(s) marked as completed.')
    mark_completed.short_description = 'Mark as Completed'
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) marked as cancelled.')
    mark_cancelled.short_description = 'Mark as Cancelled'
