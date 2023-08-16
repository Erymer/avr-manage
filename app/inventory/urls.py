"""
URL mappings for inventory app.
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from inventory import views
 
router = DefaultRouter()
router.register('equipment_type', views.EquipmentTypeViewSet)
router.register('equipment_model', views.EquipmentModelViewSet)
router.register('equipment_brand', views.EquipmentBrandViewSet)
router.register('equipment', views.EquipmentViewSet)

app_name = 'inventory'

urlpatterns = [
    path('', include(router.urls)),
]
