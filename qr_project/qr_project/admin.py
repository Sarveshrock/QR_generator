from django.contrib import admin
from .models import QRCode, UserProfile

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('words', 'qr_code_image', 'generated_at', 'get_username', 'get_organization_name', 'get_employee_id')
    readonly_fields = ('generated_at',)

    # Define methods to access User and UserProfile fields
    def get_username(self, obj):
        return obj.userprofile.user.username if hasattr(obj, 'userprofile') else "N/A"
    get_username.short_description = 'Username'

    def get_organization_name(self, obj):
        return obj.userprofile.organization_name if hasattr(obj, 'userprofile') else "N/A"
    get_organization_name.short_description = 'Organization Name'

    def get_employee_id(self, obj):
        return obj.userprofile.employee_id if hasattr(obj, 'userprofile') else "N/A"
    get_employee_id.short_description = 'Employee ID'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_name', 'employee_id')
