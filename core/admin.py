from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.db import models
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator

from apps.business.utils.segment_utils import create_default_segments

class DummyModel(models.Model):
    class Meta:
        managed = False
        verbose_name = "Página de Comandos"
        verbose_name_plural = "Páginas de Comandos"

@admin.register(DummyModel)
class CustomAdminPage(admin.ModelAdmin):
    change_list_template = "core/admin/list_commands.html"
    
    def get_queryset(self, request):
        return DummyModel.objects.none()
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("run-task/", self.admin_site.admin_view(self.run_task), name="run-task"),
        ]
        return custom_urls + urls

    @csrf_exempt
    def run_task(self, request):
        if request.method == "POST":
            method = getattr(self, request.POST.get('command_id'))
            method(request)
            self.message_user(request, "Task completed!", messages.SUCCESS)
            return HttpResponseRedirect("../")
        else:
            self.message_user(request, "Method not allowed", messages.ERROR)
            return HttpResponseRedirect("../")

    def command_generate_segments(self, request):
        create_default_segments()
