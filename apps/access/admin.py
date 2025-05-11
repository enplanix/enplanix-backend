from django.contrib import admin
from .models import AccessPreference

@admin.register(AccessPreference)
class AccessPreferencesAdmin(admin.ModelAdmin):
    search_fields = ['user__email']
    list_display = ['user__email', 'current_business']