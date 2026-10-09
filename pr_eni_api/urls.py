
from django.urls import path, include
from app_convocatorias.views import capacitacion_form_page, convocatoria_form_page, index_page

urlpatterns = [
    path('', index_page, name='index'),
    path('formulario_convocatoria.html', convocatoria_form_page, name='formulario_convocatoria'),
    path('formulario_capacitacion.html', capacitacion_form_page, name='formulario_capacitacion'),
    path('api/', include('app_convocatorias.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
