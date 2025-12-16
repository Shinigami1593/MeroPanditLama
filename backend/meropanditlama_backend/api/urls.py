from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.accounts.urls')),
    path('api/', include('api.providers.urls')),
    path('api/', include('api.bookings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "MeroPanditLama Administration"
admin.site.site_title = "MeroPanditLama Admin"
admin.site.index_title = "Welcome to MeroPanditLama Admin"