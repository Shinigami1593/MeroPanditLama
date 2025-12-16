from django.contrib import admin
from .models import Service, ServiceProvider, AvailabilitySlot, Review

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ne', 'default_price', 'created_at']
    search_fields = ['name', 'name_ne', 'description']
    list_filter = ['created_at']
    ordering = ['name']

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [
        'get_provider_name', 'religion_type', 'location',
        'experience_years', 'price_per_service', 'verified', 'created_at'
    ]
    list_filter = ['religion_type', 'verified', 'location', 'created_at']
    search_fields = [
        'user__first_name', 'user__last_name',
        'user__email', 'location', 'short_description'
    ]
    filter_horizontal = ['services']
    readonly_fields = ['created_at', 'updated_at', 'average_rating', 'total_reviews']
    
    fieldsets = (
        ('Provider Information', {
            'fields': ('user', 'religion_type', 'experience_years')
        }),
        ('Location & Services', {
            'fields': ('location', 'services', 'price_per_service')
        }),
        ('Description', {
            'fields': ('short_description', 'short_description_ne')
        }),
        ('Status', {
            'fields': ('verified',)
        }),
        ('Statistics', {
            'fields': ('average_rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_verified', 'mark_unverified']
    
    def get_provider_name(self, obj):
        return obj.user.get_full_name()
    get_provider_name.short_description = 'Provider Name'
    get_provider_name.admin_order_field = 'user__first_name'
    
    def mark_verified(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(request, f'{updated} provider(s) marked as verified.')
    mark_verified.short_description = 'Mark selected as verified'
    
    def mark_unverified(self, request, queryset):
        updated = queryset.update(verified=False)
        self.message_user(request, f'{updated} provider(s) marked as unverified.')
    mark_unverified.short_description = 'Mark selected as unverified'

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = [
        'get_provider_name', 'date', 'start_time',
        'end_time', 'is_booked', 'created_at'
    ]
    list_filter = ['is_booked', 'date', 'created_at']
    search_fields = ['provider__user__first_name', 'provider__user__last_name']
    date_hierarchy = 'date'
    ordering = ['-date', 'start_time']
    
    def get_provider_name(self, obj):
        return obj.provider.user.get_full_name()
    get_provider_name.short_description = 'Provider'
    get_provider_name.admin_order_field = 'provider__user__first_name'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'get_user_name', 'get_provider_name',
        'rating', 'created_at'
    ]
    list_filter = ['rating', 'created_at']
    search_fields = [
        'user__first_name', 'user__last_name',
        'provider__user__first_name', 'provider__user__last_name',
        'comment'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    get_user_name.short_description = 'User'
    
    def get_provider_name(self, obj):
        return obj.provider.user.get_full_name()
    get_provider_name.short_description = 'Provider'