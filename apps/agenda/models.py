from django.db import models
from core.managers import BusinessFilterMixin, CustomManager
from core.models import UUIDChronoModel, UUIDModel
from django.core.exceptions import ValidationError


class Agenda(UUIDChronoModel):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    
    observations = models.TextField(blank=True)
    created_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_agendas')
    
    objects: CustomManager = CustomManager()

    def clean(self):
        if self.start > self.end:
            raise ValidationError("Início não pode ser maior que o fim.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class AgendaExtra(UUIDModel):
    agenda = models.OneToOneField(Agenda, on_delete=models.CASCADE, blank=True, null=True, related_name='extra')
    client = models.ForeignKey('management.Client', on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey('management.Service', on_delete=models.SET_NULL, null=True, blank=True)
    use_service_duration = models.BooleanField(default=False)