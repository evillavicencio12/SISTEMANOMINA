from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from .models import Cargo, Empleado, Departamento, Rol, TipoContrato
from .forms import CargoForm, DepartamentoForm, EmpleadoForm, RolForm, TipoContratoForm, CustomUserCreationForm, CustomLoginForm
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')


@login_required
def Inicio(request):
    return render(request, 'home.html')

@login_required
def Lista(request):
    search_query = request.GET.get('q', '')
    empleados = Empleado.objects.all()

    if search_query:
        empleados = empleados.filter(nombre__icontains=search_query)

    paginator = Paginator(empleados, 10)  # 10 empleados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'empleados': page_obj,
        'search_query': search_query,
    }
    return render(request, 'empleado/empleado_list.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('core:Inicio')
    else:
        form = CustomUserCreationForm()
    return render(request, 'seguridad/register.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('core:Inicio')
    else:
        form = CustomLoginForm()
    return render(request, 'seguridad/login.html', {'form': form})

def singout(request):
    auth_logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('core:Inicio')

@login_required
def Departamentos(request):
    search_query = request.GET.get('q', '').strip()
    departamentos = Departamento.objects.all()

    if search_query:
        departamentos = departamentos.filter(descripcion__icontains=search_query)

    paginator = Paginator(departamentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'departamentos': page_obj,
        'search_query': search_query,
        'model_name': 'departamento',
        'title': 'Listado de Departamentos',
        # Otros campos si quieres
    }

    return render(request, 'departamento/departamento_list.html', context)
@login_required
def Cargos(request):
    cargos = Cargo.objects.all()
    search_query = request.GET.get('q', '')
    if search_query:
        cargos = cargos.filter(descripcion__icontains=search_query)
    paginator = Paginator(cargos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cargo/cargo_list.html', {
        'cargos': page_obj,
        'search_query': search_query,
        'model_name': 'cargo',
        'title': 'Listado de Cargos',
        'fields': ['descripcion', 'codigo']  # Puedes personalizar aquí qué campos mostrar
    })

@login_required
def vista_contratos(request):
    tipo_contratos = TipoContrato.objects.all()
    search_query = request.GET.get('q', '')
    if search_query:
        tipo_contratos = tipo_contratos.filter(descripcion__icontains=search_query)
    paginator = Paginator(tipo_contratos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tipoContrato/tipoContrato_list.html', {'tipo_contratos': page_obj, 'search_query': search_query})

@login_required
@login_required
def Nominas(request):
    roles = Rol.objects.all()
    search_query = request.GET.get('q', '')
    if search_query:
        roles = roles.filter(
            Q(empleado__nombre__icontains=search_query) | Q(empleado__cedula__icontains=search_query)
        )
    paginator = Paginator(roles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'rol/rol_list.html', {
        'objects': page_obj,
        'search_query': search_query,
        'model_name': 'nomina',
        'title': 'Listado de Roles de Pago',
    })

# Vistas de crear
@login_required
def CrearCargo(request):
    context = {'title': 'Ingresar Cargo'}
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo creado correctamente')
            return redirect('core:Cargos')
    else:
        form = CargoForm()
    context['form'] = form
    return render(request, 'cargo/cargo_create.html', context)

@login_required
def delete_cargo(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        cargo.delete()
        return redirect('core:Cargos')
    return render(request, 'cargo/cargo_delete.html', {'cargo': cargo})
@login_required
def CrearEmpleado(request):
    context = {'title': 'Ingresar Empleado'}
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado correctamente')
            return redirect('core:Lista')
    else:
        form = EmpleadoForm()
    context['form'] = form
    return render(request, 'empleado/empleado_create.html', context)

@login_required
def CrearDepartamento(request):
    context = {'title': 'Ingresar Departamento'}
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento creado correctamente')
            return redirect('core:Departamentos')
    else:
        form = DepartamentoForm()
    context['form'] = form
    return render(request, 'departamento/departamento_create.html', context)

@login_required
def CrearContrato(request):
    context = {'title': 'Ingresar Tipo de Contrato'}
    if request.method == 'POST':
        form = TipoContratoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de contrato creado correctamente')
            return redirect('core:Contrato')
    else:
        form = TipoContratoForm()
    context['form'] = form
    return render(request, 'tipoContrato/tipoContrato_create.html', context)

@login_required
def CrearNominas(request):
    context = {'title': 'Ingresar Rol de Pago'}
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol de pago creado correctamente')
            return redirect('core:Nominas')
    else:
        form = RolForm()
    context['form'] = form
    return render(request, 'rol/rol_create.html', context)

# Vistas de actualizar
@login_required
def UpdateCargo(request, id):
    cargo = get_object_or_404(Cargo, pk=id)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo actualizado correctamente')
            return redirect('core:Cargos')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'cargo/cargo_update.html', {'form': form})

@login_required
def UpdateEmpleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado correctamente')
            return redirect('core:Lista')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleado/empleado_update.html', {'form': form})

@login_required
def UpdateDepartamento(request, id):
    departamento = get_object_or_404(Departamento, pk=id)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento actualizado correctamente')
            return redirect('core:Departamentos')
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'departamento/departamento_update.html', {'form': form})

@login_required
def UpdateContrato(request, id):
    tipo_contrato = get_object_or_404(TipoContrato, pk=id)
    if request.method == 'POST':
        form = TipoContratoForm(request.POST, instance=tipo_contrato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de contrato actualizado correctamente')
            return redirect('core:Contrato')  # <-- Cambia aquí si tienes otro nombre para la lista
    else:
        form = TipoContratoForm(instance=tipo_contrato)
    return render(request, 'tipoContrato/tipoContrato_update.html', {'form': form})

@login_required
def DeleteContrato(request, id):
    contrato = get_object_or_404(TipoContrato, pk=id)

    if request.method == 'POST':
        contrato.delete()
        messages.success(request, 'Tipo de contrato eliminado correctamente.')
        return redirect('core:Contrato')  # Asegúrate que este sea el nombre correcto para la lista de contratos

    return render(request, 'tipoContrato/tipoContrato_delete.html', {
        'contrato': contrato,
        'title': f'Eliminar Tipo de Contrato: {contrato.nombre}',
    })

@login_required
def UpdateNomina(request, id):
    rol = get_object_or_404(Rol, pk=id)
    context = {'title': 'Actualizar Rol de Pago'}
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol de pago actualizado correctamente')
            return redirect('core:Nominas')
    else:
        form = RolForm(instance=rol)
    context['form'] = form
    return render(request, 'rol/rol_update.html', context)

# Vistas de eliminar
@login_required
def Eliminar(request, id, modelo):
    modelo_lower = modelo.lower()

    if modelo_lower == "empleado":
        obj = get_object_or_404(Empleado, pk=id)
        template = 'empleado/empleado_delete.html'
        redirect_url = 'core:Lista'
    elif modelo_lower == "nomina":
        obj = get_object_or_404(Rol, pk=id)
        template = 'rol/rol_delete.html'
        redirect_url = 'core:Nominas'
    elif modelo_lower == "cargo":
        obj = get_object_or_404(Cargo, pk=id)
        template = 'cargo/cargo_delete.html'
        redirect_url = 'core:Cargos'
    elif modelo_lower == "departamento":
        obj = get_object_or_404(Departamento, pk=id)
        template = 'departamento/departamento_delete.html'
        redirect_url = 'core:Departamentos'
    elif modelo_lower == "contrato":
        obj = get_object_or_404(TipoContrato, pk=id)
        template = 'tipoContrato/tipoContrato_delete.html'
        redirect_url = 'core:Contrato'
    else:
        messages.error(request, 'Modelo no válido.')
        return redirect('core:Inicio')

    if request.method == 'POST':
        obj.delete()
        messages.success(request, f'{modelo.capitalize()} eliminado correctamente.')
        return redirect(redirect_url)
    return render(request, template, {modelo_lower: obj})

def DeleteDepartamento(request, id):
    departamento = get_object_or_404(Departamento, id=id)

    if request.method == 'POST':
        departamento.delete()
        return redirect(reverse('core:ListadoDepartamento'))  # Ajusta este nombre a tu URL de listado

    return render(request, 'core/delete_departamento.html', {
        'departamento': departamento,
        'title': f'Eliminar Departamento: {departamento.nombre}',  # o el campo que uses para mostrar
    })
@login_required
def DeleteEmpleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)

    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado correctamente.')
        return redirect('core:Lista')  # URL de la lista de empleados

    return render(request, 'empleado/empleado_delete.html', {
        'empleado': empleado,
        'title': f'Eliminar Empleado: {empleado.nombre}',
    })
@login_required
def DeleteNomina(request, id):
    rol = get_object_or_404(Rol, pk=id)
    if request.method == 'POST':
        rol.delete()
        messages.success(request, 'Rol eliminado correctamente.')
        return redirect('core:Nominas')
    return render(request, 'rol/rol_delete.html', {'rol': rol})
