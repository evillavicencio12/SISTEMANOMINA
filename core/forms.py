from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Cargo, Empleado, Rol, TipoContrato, Departamento

class CustomUserCreationForm(UserCreationForm):
    primer_nombre = forms.CharField(max_length=100, required=True, label="Primer Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=100, required=True, label="Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CargoForm(forms.ModelForm):
    descripcion = forms.CharField(
        label="Descripción del Cargo",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la descripción del cargo',
            'autocomplete': 'off',
        }),
        help_text="Máximo 100 caracteres."
    )
    nivel = forms.IntegerField(
        label="Nivel Jerárquico",
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Nivel jerárquico del cargo (1-10)"
    )
    responsabilidades = forms.CharField(
        label="Responsabilidades",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        help_text="Responsabilidades y funciones del cargo"
    )
    salario_base = forms.DecimalField(
        label="Salario Base",
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Salario base recomendado"
    )

    class Meta:
        model = Cargo
        fields = ['descripcion', 'nivel', 'responsabilidades', 'salario_base']

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion:
            descripcion = descripcion.strip()
            if len(descripcion) < 3:
                raise forms.ValidationError("La descripción debe tener al menos 3 caracteres.")
        return descripcion
class EmpleadoForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    cedula = forms.CharField(label="Cédula", widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label="Dirección", widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexo = forms.ChoiceField(
        choices=Empleado.SEXO_CHOICES,
        label="Sexo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sueldo = forms.DecimalField(label="Sueldo", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        label="Cargo",
        empty_label="Seleccione el cargo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label="Departamento",
        empty_label="Seleccione su departamento",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tipo_contrato = forms.ModelChoiceField(
        queryset=TipoContrato.objects.all(),
        label="Tipo de Contrato",
        empty_label="Seleccione su tipo de contrato",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Empleado
        fields = ['nombre', 'cedula', 'direccion', 'sexo', 'sueldo', 'cargo', 'departamento', 'tipo_contrato']

class DepartamentoForm(forms.ModelForm):
    descripcion = forms.CharField(label="Descripción", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Departamento
        fields = ['descripcion']

class TipoContratoForm(forms.ModelForm):
    descripcion = forms.CharField(label="Descripción", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = TipoContrato
        fields = ['descripcion']

class RolForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        label="Empleado",
        empty_label="Seleccione el empleado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    anio_mes = forms.DateField(label="Año y Mes", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    sueldo = forms.DecimalField(label="Sueldo", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    horas_extra = forms.DecimalField(label="Horas Extras", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    bono = forms.DecimalField(label="Bono", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Rol
        fields = ['empleado', 'anio_mes', 'sueldo', 'horas_extra', 'bono']