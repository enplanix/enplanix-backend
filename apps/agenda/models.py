from django.db import models
from core.models import UUIDChronoModel, UUIDModel


class Agenda(UUIDChronoModel):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    
    observations = models.TextField(blank=True)


class AgendaExtra(UUIDModel):
    agenda = models.OneToOneField(Agenda, on_delete=models.CASCADE, blank=True, null=True, related_name='extra')
    client = models.ForeignKey('management.Client', on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey('management.Service', on_delete=models.SET_NULL, null=True, blank=True)
    use_service_duration = models.BooleanField(default=False)