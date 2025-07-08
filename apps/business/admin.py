from django.contrib import admin
from .models import Business, BusinessConfig, BusinessMember, Indicator, Segment



@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'emoji']

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']


@admin.register(BusinessConfig)
class BusinessConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessMember)
class BusinessMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__email', 'business__name']


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'formula', 'description', 'value']