from django.db.models import signals
from django.dispatch import receiver
from apps.sale.models import Sale, ServiceSaleItem
from django.db import transaction


@transaction.atomic
def generate_default_sale_for_agenda(agenda_extra):
    new_sale, created_new_sale = Sale.objects.get_or_create(
        business=agenda_extra.agenda.business, 
        agenda_extra=agenda_extra, 
        created_by=agenda_extra.agenda.created_by
    )
    if created_new_sale:
        ServiceSaleItem.objects.create(sale=new_sale, quantity=1, origin=agenda_extra.service)


def update_agenda_service(instance):
    service = ServiceSaleItem.objects.filter(sale__agenda_extra=instance).order_by('created_at').first()
    service.origin = instance.service
    service.save()


@receiver(signals.post_save, sender='agenda.AgendaExtra')
def add_business_default_categories(instance, created=True, **kwargs):
    if created:
        return generate_default_sale_for_agenda(instance)
    update_agenda_service(instance)