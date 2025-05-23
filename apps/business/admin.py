from django.contrib import admin
from .models import Business, BusinessConfig, BusinessMember, Segment



@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'emoji']

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessConfig)
class BusinessConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessMember)
class BusinessMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__email', 'business__name']
