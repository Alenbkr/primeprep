from rest_framework import viewsets
from .models import Dish, Ration
from .serializer import DishSerializer, RationSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class RationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RationSerializer

    def get_queryset(self):
        queryset = Ration.objects.filter(is_active=True).prefetch_related('rationdish_set__dish')
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(calories_tag=tag)
        return queryset
