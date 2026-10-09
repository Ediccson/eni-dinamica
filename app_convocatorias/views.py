from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Convocatoria
from .serializers import ConvocatoriaSerializer


def index_page(request):
    html = (settings.BASE_DIR / 'index.html').read_text(encoding='utf-8')
    return HttpResponse(html, content_type='text/html; charset=utf-8')


def convocatoria_form_page(request):
    html = (settings.BASE_DIR / 'formulario_convocatoria.html').read_text(encoding='utf-8')
    return HttpResponse(html, content_type='text/html; charset=utf-8')


def capacitacion_form_page(request):
    html = (settings.BASE_DIR / 'formulario_capacitacion.html').read_text(encoding='utf-8')
    return HttpResponse(html, content_type='text/html; charset=utf-8')


class ConvocatoriaListCreateView(viewsets.ModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer
    permission_classes = [IsAuthenticated]
