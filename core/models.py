from django.db import models

# Create your models here.
class Cargo(models.Model):
    # Descripción del cargo o puesto que ocupa un empleado en la empresa
    descripcion = models.CharField(max_length=100, unique=True, help_text="Nombre o descripción del cargo")

    # Opcional: un campo para el nivel jerárquico del cargo (por ejemplo, 1 = bajo, 5 = alto)
    nivel = models.PositiveSmallIntegerField(default=1, help_text="Nivel jerárquico del cargo (1-10)")

    # Opcional: una breve descripción de las responsabilidades principales del cargo
    responsabilidades = models.TextField(blank=True, help_text="Responsabilidades y funciones del cargo")

    # Opcional: salario base recomendado para este cargo (puede ayudar para validaciones o reportes)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Salario base recomendado")

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['nivel', 'descripcion']

class Departamento(models.Model):
    descripcion = models.CharField(max_length=100)
    def __str__(self):
        return self.descripcion

class TipoContrato(models.Model):
    descripcion = models.CharField(max_length=100)
    def __str__(self):
        return self.descripcion


class Empleado(models.Model):
    SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ]

    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    direccion = models.TextField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento,
    on_delete=models.CASCADE)
    tipo_contrato = models.ForeignKey(TipoContrato,
    on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    aniomes = models.DateField()#202501
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    horas_extra = models.DecimalField(max_digits=10, decimal_places=2)
    bono = models.DecimalField(max_digits=10, decimal_places=2)
    iess = models.DecimalField(max_digits=10, decimal_places=2)
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2)
    neto = models.DecimalField(max_digits=10, decimal_places=2)
