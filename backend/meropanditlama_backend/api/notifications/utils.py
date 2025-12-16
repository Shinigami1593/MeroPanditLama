from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_booking_notification(booking, notification_type, recipient):
    """
    Send email notification for booking events.
    
    Args:
        booking: Booking instance
        notification_type: 'requested', 'confirmed', 'cancelled', 'reminder'
        recipient: User instance to send email to
    """
    
    language = recipient.language_pref
    
    # Email templates
    template_map = {
        'requested': f'emails/booking_requested_{language}.html',
        'confirmed': f'emails/booking_confirmed_{language}.html',
        'cancelled': f'emails/booking_cancelled.html',  # Same for both languages
        'reminder': f'emails/booking_reminder_{language}.html',
    }
    
    # Email subjects
    subject_map = {
        'en': {
            'requested': 'New Booking Request - MeroPanditLama',
            'confirmed': 'Booking Confirmed - MeroPanditLama',
            'cancelled': 'Booking Cancelled - MeroPanditLama',
            'reminder': 'Booking Reminder - MeroPanditLama',
        },
        'ne': {
            'requested': 'नयाँ बुकिंग अनुरोध - MeroPanditLama',
            'confirmed': 'बुकिंग पुष्टि भयो - MeroPanditLama',
            'cancelled': 'बुकिंग रद्द भयो - MeroPanditLama',
            'reminder': 'बुकिंग सम्झना - MeroPanditLama',
        }
    }
    
    try:
        # Prepare context
        context = {
            'booking': booking,
            'recipient': recipient,
            'user_name': booking.user.get_full_name(),
            'provider_name': booking.provider.user.get_full_name(),
            'provider_phone': booking.provider.user.phone,
            'provider_location': booking.provider.location,
            'service_name': booking.service.name if booking.service else 'Service',
            'requested_datetime': booking.requested_datetime.strftime('%B %d, %Y at %I:%M %p'),
            'duration_minutes': booking.duration_minutes,
            'notes': booking.notes,
            'cancellation_reason': booking.cancellation_reason,
            'booking_url': f"{settings.FRONTEND_URL}/bookings/{booking.id}",
        }
        
        # Render email
        template = template_map.get(notification_type)
        html_message = render_to_string(template, context)
        
        # Get subject
        subject = subject_map.get(language, subject_map['en']).get(
            notification_type,
            'MeroPanditLama Notification'
        )
        
        # Send email
        send_mail(
            subject=subject,
            message='',  # Plain text version
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(
            f"Email sent: {notification_type} to {recipient.email} for booking #{booking.id}"
        )
        
    except Exception as e:
        logger.error(
            f"Failed to send email: {notification_type} to {recipient.email}. Error: {str(e)}"
        )