from django.contrib import admin
from django.urls import path
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static for media files
from . import views
from qr_project.views import generate_qr, home, signup, signin , customize_qr,dashboard # Ensure your views are imported correctly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Your home view
    path('generate/', generate_qr, name='generate_qr'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),  # QR code generation view
    path('Customize/', customize_qr, name='Customize'),
    path('dashboard/', dashboard, name='dashboard'),    # QR code generation view
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
