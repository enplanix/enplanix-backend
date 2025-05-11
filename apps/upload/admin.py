from django.contrib import admin
from .models import ImageUpload, FileUpload


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file']


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file']