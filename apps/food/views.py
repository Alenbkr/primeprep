from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Dish, Ration
from .serializer import DishSerializer, RationSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminUser]


class RationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Ration.objects.filter(is_active=True).prefetch_related('rationdish_set__dish')
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(calories_tag=tag)
        return queryset
