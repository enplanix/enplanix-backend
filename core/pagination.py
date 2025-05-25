from rest_framework.pagination import PageNumberPagination
from django.db.models import Case, When, Value, IntegerField

class ConditionalPagination(PageNumberPagination):
    
    def get_queryset_ordering(self, queryset):
        if queryset.query.order_by:
            return list(queryset.query.order_by)
        
        return getattr(queryset.model._meta, 'ordering', [])

    def paginate_queryset(self, queryset, request, view=None):
        if 'page' not in request.query_params:
            return None
        ids = request.query_params.get('ids', None)
        if ids:
            ids = ids.split(',')
            old_ordering = self.get_queryset_ordering(queryset)
            ordering = Case(
                *[When(id=uuid, then=Value(index)) for index, uuid in enumerate(ids)],
                default=len(ids),
                output_field=IntegerField()
            )
            queryset = queryset.annotate(custom_ordering=ordering).order_by('custom_ordering', *old_ordering)
        return super().paginate_queryset(queryset, request, view)
