from django.shortcuts import render
from .models import Dish, RationDish, Ration
from rest_framework import viewsets
from .serializer import DishSerializer

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    
    
