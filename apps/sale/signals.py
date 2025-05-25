from django.db.models import signals
from django.dispatch import receiver
from apps.sale.models import Sale, SaleItem
from django.db import transaction


@transaction.atomic
def generate_default_sale_for_agenda(agenda_extra):
    sale, created_new_sale = Sale.objects.update_or_create(
        business=agenda_extra.agenda.business, 
        agenda_extra=agenda_extra, 
        client=agenda_extra.client,
        created_by=agenda_extra.agenda.created_by,
    )
    if created_new_sale:
        SaleItem.objects.create(sale=sale, quantity=1, origin=agenda_extra.service)
    sale.update_total_price()

def update_agenda_service(instance):
    Sale.objects.filter(agenda_extra=instance).update(
        client=instance.client
    )

    service = SaleItem.objects.filter(sale__agenda_extra=instance).order_by('created_at').first()
    if service:
        service.origin = instance.service
        service.save()
        service.sale.update_total_price()


@receiver(signals.post_save, sender='agenda.AgendaExtra')
def add_business_default_categories(instance, created=True, **kwargs):
    if created:
        return generate_default_sale_for_agenda(instance)
    update_agenda_service(instance)