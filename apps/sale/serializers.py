from email.policy import default
from rest_framework import serializers

from apps.access.serializers import UserSerializer
from apps.management.models import Offer
from apps.management.serializers import ClientSerializer
from core.serializers import DynamicFieldsModelSerializer
from .models import Sale, SaleItem


class SaleItemSlimSerializer(DynamicFieldsModelSerializer):
    
    id = serializers.UUIDField(required=False)  # Make id writable and optional
    code = serializers.CharField(source='snapshot_code', default='', read_only=True)
    name = serializers.CharField(source='snapshot_name', default='', read_only=True)
    price = serializers.CharField(source='snapshot_price', default='', read_only=True)
    type = serializers.CharField(source='origin.type', read_only=True)
    cover = serializers.CharField(source='origin.cover.id', default='', read_only=True)

    class Meta:
        model = SaleItem
        fields = ['id', 'code', 'name', 'price', 'quantity', 'type', 'cover', 'origin']

    def create(self, validated_data):
        return super().create(validated_data)

    def save(self, **kwargs):
        return super().save(**kwargs)

class SaleSerializer(DynamicFieldsModelSerializer):

    user_data = UserSerializer(source='created_by', read_only=True)
    client_data = ClientSerializer(source='client', read_only=True)
    
    sale_items_read = SaleItemSlimSerializer(source='sale_items', many=True, read_only=True)
    sale_items = SaleItemSlimSerializer(many=True, write_only=True, required=False, fields=['id', 'quantity', 'origin'])
    
    class Meta:
        model = Sale
        exclude = ['business', 'created_by']
        read_only_fields = ['status']

    def update_sale_items(self, sale, sale_items):
        if sale_items is None:
            return
        keep = []
        for sale_item in sale_items:
            index = sale_item.pop("id", None)
            if index:
                SaleItem.objects.filter(id=index).update(
                    **sale_item,
                )
                keep.append(index)
            else:
                item = SaleItem.objects.create(sale=sale, **sale_item)
                keep.append(item.id)
        SaleItem.objects.filter(sale=sale).exclude(id__in=keep).delete()

    def create(self, validated_data):
        sale_items = validated_data.pop('sale_items', None)
        instance = super().create(validated_data)
        self.update_sale_items(instance, sale_items)
        return instance
        
    def update(self, instance, validated_data):
        sale_items = validated_data.pop('sale_items', None)
        instance = super().update(instance, validated_data)
        self.update_sale_items(instance, sale_items)
        return instance
