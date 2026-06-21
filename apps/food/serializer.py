from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Dish, Ration, RationDish


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"


class RationDishSerializer(ModelSerializer):
    dish = DishSerializer(read_only=True)
    total_calories = serializers.IntegerField(read_only=True)
    total_protein = serializers.FloatField(read_only=True)
    total_fat = serializers.FloatField(read_only=True)
    total_carbs = serializers.FloatField(read_only=True)

    class Meta:
        model = RationDish
        fields = ['id', 'dish', 'weight', 'day_number',
                  'total_calories', 'total_protein', 'total_fat', 'total_carbs']


class RationSerializer(ModelSerializer):
    rationdish_set = RationDishSerializer(many=True, read_only=True)

    class Meta:
        model = Ration
        fields = ['id', 'name', 'calories_tag', 'price', 'is_active', 'rationdish_set']
