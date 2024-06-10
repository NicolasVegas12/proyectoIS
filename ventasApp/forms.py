from django import forms 
from django.forms import fields 
from .models import *
from django.contrib.auth.models import User
import datetime

#Formulario "Actualizar Perfil"
class PerfilForm(forms.Form):
    last_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    email = forms.EmailField()

#Formulario "Nuevo Usuario"
class UsuarioForm(forms.Form):
    last_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=120,widget=forms.PasswordInput)
    is_superuser = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)

#Formulario "Editar Usuario"
class UsuarioEditForm(forms.Form):
    last_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    is_superuser = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)


class GroupForm(forms.Form):
    name = forms.CharField(max_length=150)

#Formulario "Nueva Categoria"
class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields=[
            'descripcion',
            'activo',
            ]

#Formulario "Nueva Cliente"
class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=[
            'tipoCliente',
            'nombres',
            'apellidos',
            'direccion',
            'email',
            'telefono',
            'tipoDocumentoIdentidad',
            'documentoIdentidad',
            'activo',
            ]

#No se muestra          
class FormaPagoForm(forms.ModelForm):
    class Meta:
        model=FormaPago
        fields=[
            'descripcion',
            'nroCuotas',
            'frecuencia',
            'interes',
            'activo',
            ]

#Formulario "Producto"     
class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=[
            'codigo',
            'categoria',      
            'nombre',
            'descripcion',
            'marca',
            'modelo',
            'stock',
            'precioUnitario',
            'urlImagen',
            'nombreImagen'
            ]
        widgets = {
            'urlImagen': forms.HiddenInput(),
            'nombreImagen': forms.HiddenInput(),
            'codigo': forms.TextInput(attrs={'readonly': True})
        }
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['categoria'].queryset = Categoria.objects.filter(activo=True)
         
#Formulario "Proveedor"
class ProveedorForm(forms.ModelForm):
    class Meta:
        model=Proveedor
        fields=[
            'ruc',
            'razonSocial',
            'nombreComercial',
            'direccion',
            'email',
            'telefono',
            'activo',
            ]

#Formulario "Nuevo Trabajador"
class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields=[
            'user',
            'nombres',
            'apellidos',
            'direccion',
            'email',
            'telefono',
            'sexo',
            'activo',
            ]
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['user'].queryset = User.objects.filter(is_active=True)

#No se muestra       
class TipoClienteForm(forms.ModelForm):
    class Meta:
        model=TipoCliente
        fields=[
            'descripcion',
            'activo',
            ]

#Formulario "Pedido de Venta"
class PedidoVentaForm(forms.ModelForm):
    class Meta:
        model = PedidoVenta
        fields=[
            'trabajador',
            'cliente',
            'formaPago',
            'codigo',
            'tipoDocumento',
            'fechaEmision',
            'fechaEntrega',
            'tipoMoneda',
            'tasaCambio',
            'tasaIgv',
            'estado'
            ]
        widgets = {            
            'fechaEmision': forms.TextInput(attrs={'type': 'date'}),
            'fechaEntrega': forms.TextInput(attrs={'type': 'date'}),
            'codigo': forms.TextInput(attrs={'readonly': True}),
            'tasaCambio':forms.NumberInput(attrs={'step': '0.01'}),            
            'tasaIgv': forms.NumberInput(attrs={'step': '0.01'})
        }
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['trabajador'].queryset = Trabajador.objects.filter(activo=True,eliminado=False)

#Formulario "Orden de Compra"
class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = [
            'trabajador',
            'proveedor',
            'formaPago',
            'codigo',
            'tipoDocumento',
            'fechaEmision',
            'fechaEntrega',
            'tipoMoneda',
            'tasaCambio',
            'tasaIgv',
            'estado',
        ]
        widgets = {
            #'trabajador': forms.ChoiceField(attrs={'defa': True}),
            'codigo': forms.TextInput(attrs={'readonly': True}),
            'fechaEmision': forms.TextInput(attrs={'type': 'date'}),
            'fechaEntrega': forms.TextInput(attrs={'type': 'date'}),
            'tasaCambio':forms.NumberInput(attrs={'step': '0.01'}),
            'tasaIgv': forms.NumberInput(attrs={'step': '0.01'})
        }
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['trabajador'].queryset = Trabajador.objects.filter(activo=True,eliminado=False)
        
class NotaAlmacenForm(forms.ModelForm):
    class Meta:
        model = NotaAlmacen
        fields = [
            'trabajador',
            'pedidoVenta',
            'ordenCompra',
            'codigo',
            'fechaEmision',
            'fechaEntrega',
            'tipoOperacion',
            'serie',
            'numero',
            'estado',
        ]
        widgets = {
            'tipoOperacion': forms.Select(attrs={'id': 'id_tipoOperacion'}),
            'serie': forms.TextInput(attrs={'readonly': True}),
            'numero': forms.TextInput(attrs={'readonly': True}),
            'codigo': forms.TextInput(attrs={'readonly': True}),
            'fechaEmision': forms.TextInput(attrs={'type': 'date'}),
            'fechaEntrega': forms.TextInput(attrs={'type': 'date'}),
            
        }