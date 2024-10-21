from django.contrib import admin
from django.urls import path
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static for media files

from qr_project.views import generate_qr, home  # Ensure your views are imported correctly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Your home view
    path('generate/', generate_qr, name='generate_qr'),  # QR code generation view
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
