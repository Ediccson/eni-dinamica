from django.db import models

# Create your models here.
class Convocatoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'convocatorias'

    def __str__(self):
        return self.nombre    
