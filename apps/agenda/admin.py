from django.contrib import admin
from .models import Agenda, AgendaExtra


class AgendaExtraInline(admin.StackedInline):
    model = AgendaExtra
    extra = 1
    raw_id_fields = ['client', 'service']


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    inlines = [AgendaExtraInline]
    list_display = ['id', 'name', 'date', 'start', 'end']

@admin.register(AgendaExtra)
class AgendaExtraAdmin(admin.ModelAdmin):
    pass