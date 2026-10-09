from django.urls import path, include
from .views import ConvocatoriaListCreateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('convocatorias', ConvocatoriaListCreateView, basename='convocatoria')

urlpatterns = [
    path('', include(router.urls)),
]
