from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'dish', DishViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]