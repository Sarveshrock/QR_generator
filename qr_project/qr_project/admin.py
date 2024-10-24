from django.contrib import admin
from .models import QRCode

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('words', 'qr_code_image', 'generated_at')
    readonly_fields = ('generated_at',)

# Alternatively, you could use:
# admin.site.register(QRCode, QRCodeAdmin)
