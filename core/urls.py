from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('empleados/', views.Lista, name='Lista'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.singout, name='singout'),
    path('departamentos/', views.Departamentos, name='Departamentos'),
    path('cargos/', views.Cargos, name='Cargos'),
    path('contratos/', views.vista_contratos, name='Contrato'),
    path('nominas/', views.Nominas, name='Nominas'),
    path('cargos/crear/', views.CrearCargo, name='CrearCargo'),
    path('empleados/crear/', views.CrearEmpleado, name='CrearEmpleado'),
    path('departamentos/crear/', views.CrearDepartamento, name='CrearDepartamento'),
    path('contratos/crear/', views.CrearContrato, name='CrearContrato'),
    path('nominas/crear/', views.CrearNominas, name='create_nomina'),
    path('cargos/update/<int:id>/', views.UpdateCargo, name='UpdateCargo'),
    path('empleados/update/<int:id>/', views.UpdateEmpleado, name='UpdateEmpleado'),
    path('empleados/delete/<int:id>/', views.DeleteEmpleado, name='DeleteEmpleado'),
    path('departamentos/update/<int:id>/', views.UpdateDepartamento, name='UpdateDepartamento'),
    path('departamentos/delete/<int:id>/', views.DeleteDepartamento, name='DeleteDepartamento'),
    path('contratos/update/<int:id>/', views.UpdateContrato, name='UpdateContrato'),
    path('contratos/delete/<int:id>/', views.DeleteContrato, name='DeleteContrato'),
    path('nominas/update/<int:id>/', views.UpdateNomina, name='UpdateNomina'),
    path('nominas/delete/<int:id>/', views.DeleteNomina, name='DeleteNomina'),
    path('eliminar/<int:id>/<str:modelo>/', views.Eliminar, name='Eliminar'),
    path('cargos/eliminar/<int:pk>/', views.delete_cargo, name='delete_cargo'),
]