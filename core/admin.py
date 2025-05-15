from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Cargo, Departamento, TipoContrato, Empleado, Rol

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    list_filter = ('descripcion',)

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    list_filter = ('descripcion',)

@admin.register(TipoContrato)
class TipoContratoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    list_filter = ('descripcion',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'sueldo', 'cargo', 'departamento', 'tipo_contrato', 'sexo')
    search_fields = ('nombre', 'cedula', 'cargo__descripcion', 'departamento__descripcion', 'tipo_contrato__descripcion')
    list_filter = ('sexo', 'cargo', 'departamento', 'tipo_contrato')
    list_per_page = 10

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'aniomes', 'sueldo', 'horas_extra', 'bono', 'tot_ing', 'iess', 'tot_des', 'neto')  # Fixed typo
    search_fields = ('empleado__nombre', 'empleado__cedula')
    list_filter = (('aniomes', admin.DateFieldListFilter), 'empleado__cargo')  # Fixed typo
    list_per_page = 10
    readonly_fields = ('tot_ing', 'iess', 'tot_des', 'neto')

def setup_permissions():
    hr_group, created = Group.objects.get_or_create(name='HR Managers')
    content_types = [
        ContentType.objects.get_for_model(Cargo),
        ContentType.objects.get_for_model(Departamento),
        ContentType.objects.get_for_model(TipoContrato),
        ContentType.objects.get_for_model(Empleado),
        ContentType.objects.get_for_model(Rol),
    ]
    permissions = Permission.objects.filter(content_type__in=content_types)
    hr_group.permissions.set(permissions)