from rest_framework import serializers
from .models import DeliveryAddress, Order


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['id', 'city', 'street', 'apartment', 'is_default']


class OrderSerializer(serializers.ModelSerializer):
    address = DeliveryAddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=DeliveryAddress.objects.all(), source='address', write_only=True
    )
    ration_name = serializers.CharField(source='ration.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'ration', 'ration_name',
            'address', 'address_id',
            'status', 'status_display',
            'start_date', 'total_price', 'created_at'
        ]
        read_only_fields = ['status', 'total_price', 'created_at']
