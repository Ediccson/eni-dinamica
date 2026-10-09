from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Convocatoria


class ConvocatoriaApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_pages_are_served_from_django(self):
        index_response = self.client.get('/')
        form_response = self.client.get('/formulario_convocatoria.html')
        training_form_response = self.client.get('/formulario_capacitacion.html')

        self.assertEqual(index_response.status_code, 200)
        self.assertContains(index_response, 'Nueva convocatoria')
        self.assertEqual(form_response.status_code, 200)
        self.assertContains(form_response, 'Crear convocatoria')
        self.assertEqual(training_form_response.status_code, 200)
        self.assertContains(index_response, 'Nueva capacitación')
        self.assertContains(training_form_response, 'Registrar capacitación')
        self.assertContains(training_form_response, '/rest/v1/capacitaciones')

    def test_create_convocatoria(self):
        get_response = self.client.get('/api/convocatorias/')
        post_response = self.client.post(
            '/api/convocatorias/',
            {
                'nombre': 'Capacitación digital',
                'descripcion': 'Programa de formación para la comunidad.',
                'fecha_inicio': '2026-11-01',
                'fecha_fin': '2026-11-30',
            },
            format='json',
        )

        self.assertEqual(get_response.status_code, 403)
        self.assertEqual(post_response.status_code, 403)
        self.assertEqual(Convocatoria.objects.count(), 0)

        user = get_user_model().objects.create_user(username='api-user')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/api/convocatorias/',
            {
                'nombre': 'Capacitación digital',
                'descripcion': 'Programa de formación para la comunidad.',
                'fecha_inicio': '2026-11-01',
                'fecha_fin': '2026-11-30',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Convocatoria.objects.count(), 1)
        self.assertEqual(Convocatoria.objects.get().nombre, 'Capacitación digital')
