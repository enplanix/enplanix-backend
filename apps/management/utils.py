


from apps.business.models import Business
from apps.management.models import Category, CategoryTemplate


def generate_business_categories():
    for business in Business.objects.all():
        templates = CategoryTemplate.objects.filter(segment=business.segment).values('name', 'type')
        [Category.objects.get_or_create(business=business, **template) for template in templates]