from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DeliveryAddress, Order
from .serializer import DeliveryAddressSerializer, OrderSerializer


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        ration = serializer.validated_data['ration']
        serializer.save(user=self.request.user, total_price=ration.price)
