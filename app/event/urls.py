"""
URL mappings for inventory app.
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from event import views
 
router = DefaultRouter()
router.register('event', views.EventViewSet)
router.register('event_photo', views.EventPhotoViewSet)

app_name = 'event'

urlpatterns = [
    path('', include(router.urls)),
]
