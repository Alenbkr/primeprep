from rest_framework.serializers import ModelSerializer
from .models import Dish, Ration, RationDish


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"
        

