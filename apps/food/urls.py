from django.urls import path, include
from rest_framework import routers
from .views import DishViewSet, RationViewSet

router = routers.SimpleRouter()
router.register(r'dish', DishViewSet)
router.register(r'rations', RationViewSet, basename='ration')

urlpatterns = [
    path('api/', include(router.urls)),
]
