from django.contrib import admin
from .models import AccessPreference, UserPreference

@admin.register(AccessPreference)
class AccessPreferencesAdmin(admin.ModelAdmin):
    search_fields = ['user__email']
    list_display = ['user__email', 'current_business']


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    search_fields = ['user__email']
    list_display = ['user__email']