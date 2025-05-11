from django.contrib import admin
from .models import Business, BusinessConfig, BusinessMember, SegmentCategory, Segment


class SegmentInline(admin.TabularInline):
    model = Segment
    extra = 1

@admin.register(SegmentCategory)
class SegmentCategoryAdmin(admin.ModelAdmin):
    inlines = [SegmentInline]
    list_display = ['code', 'name']

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessConfig)
class BusinessConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessMember)
class BusinessMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__email', 'business__name']
