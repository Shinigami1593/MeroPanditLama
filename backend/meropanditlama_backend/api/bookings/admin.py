from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'user', 
        'provider', 
        'service',
        'requested_date',
        'time_slot',
        'status', 
        'created_at'
    ]
    
    list_filter = [
        'status', 
        'time_slot',
        'created_at', 
        'requested_date'
    ]
    
    search_fields = [
        'user__email', 
        'user__first_name', 
        'user__last_name',
        'provider__user__first_name', 
        'provider__user__last_name',
        'notes'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'provider', 'service')
        }),
        ('Schedule', {
            'fields': ('requested_date', 'time_slot', 'duration_minutes')
        }),
        ('Status', {
            'fields': ('status', 'notes', 'cancellation_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 
            'provider__user', 
            'service'
        )