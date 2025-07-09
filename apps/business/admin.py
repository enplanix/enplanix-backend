from django.contrib import admin

from apps.business.utils.category_utils import create_default_categories
from apps.business.utils.indicator_utils import create_default_indicators
from .models import Business, BusinessConfig, BusinessMember, Indicator, Segment
from django.db import transaction
from django.contrib import messages


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'emoji']


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    actions = ['generate_indicators', 'generate_categories']

    @admin.action(description='Generates indicators for the following business')
    def generate_indicators(modeladmin, request, queryset):
        try:
            with transaction.atomic():
                for business in queryset:
                    create_default_indicators(business)
                messages.success(request, 'Indicators created successfully')
        except Exception as e:
            messages.error(request, str(e))

    @admin.action(description='Generates categories for the following business')
    def generate_categories(modeladmin, request, queryset):
        try:
            with transaction.atomic():
                for business in queryset:
                    create_default_categories(business)
                messages.success(request, 'Indicators created successfully')
        except Exception as e:
            messages.error(request, str(e))


@admin.register(BusinessConfig)
class BusinessConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessMember)
class BusinessMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__email', 'business__name']


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'formula', 'description', 'value', 'business']
    list_filter = ['business']
