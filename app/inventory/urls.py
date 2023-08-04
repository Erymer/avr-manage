"""
URL mappings for equipment app.
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from inventory import views
 
router = DefaultRouter()
router.register('equipment_type', views.EquipmentTypeViewSet)
# router.register('equipment', views.EquipmentViewSet)
# router.register('equipment-model', views.EquipmentModelViewSet)
# router.register('equipment-brand', views.EquipmentBrandViewSet)

app_name = 'inventory'

urlpatterns = [
    path('', include(router.urls)),
]
