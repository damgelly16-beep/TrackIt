from django import forms
from .models import Usuario, Rol, Productos, Grupo, Proveedor

# formulario de ingreso
class LoginForm(forms.Form):
    TxtUsuario = forms.CharField(
        label="Usuario",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: admin o 1088123456'})
    )
    TxtPassword = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'TxtCaja', 'placeholder': '••••••••'})
    )

# creacion de usuarios nuevos
class UsuarioForm(forms.ModelForm):
    fk_codrol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        required=False,
        label="Rol del Usuario",
        empty_label="-- Seleccione un Rol --",
        widget=forms.Select(attrs={'class': 'TxtCaja'})
    )

    class Meta:
        model = Usuario
        fields = ['numcedula', 'nombreusuario1', 'nombreusuario2', 'apellidousuario1', 'apellidousuario2', 'emailusuario', 'fk_codrol']
        labels = {
            'numcedula': 'Número de Cédula',
            'nombreusuario1': 'Primer Nombre',
            'nombreusuario2': 'Segundo Nombre',
            'apellidousuario1': 'Primer Apellido',
            'apellidousuario2': 'Segundo Apellido',
            'emailusuario': 'Correo Electrónico',
        }
        widgets = {
            'numcedula': forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: 1088123456'}),
            'nombreusuario1': forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Carlos'}),
            'nombreusuario2': forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Andrés'}),
            'apellidousuario1': forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Pérez'}),
            'apellidousuario2': forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Gómez'}),
            'emailusuario': forms.EmailInput(attrs={'class': 'TxtCaja', 'placeholder': 'ejemplo@correo.com'}),
        }

# edicion de datos de usuario
class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombreusuario1', 'nombreusuario2', 'apellidousuario1', 'apellidousuario2', 'emailusuario', 'fk_codrol']
        labels = {
            'nombreusuario1': 'Primer Nombre',
            'nombreusuario2': 'Segundo Nombre',
            'apellidousuario1': 'Primer Apellido',
            'apellidousuario2': 'Segundo Apellido',
            'emailusuario': 'Correo Electrónico',
            'fk_codrol': 'Rol del Usuario',
        }
        widgets = {
            'nombreusuario1': forms.TextInput(attrs={'class': 'TxtCaja'}),
            'nombreusuario2': forms.TextInput(attrs={'class': 'TxtCaja'}),
            'apellidousuario1': forms.TextInput(attrs={'class': 'TxtCaja'}),
            'apellidousuario2': forms.TextInput(attrs={'class': 'TxtCaja'}),
            'emailusuario': forms.EmailInput(attrs={'class': 'TxtCaja'}),
            'fk_codrol': forms.Select(attrs={'class': 'TxtCaja'}),
        }

# asignacion de roles a usuarios
class AsignarPermisosForm(forms.Form):
    numCedula = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label="Seleccionar Usuario (Cédula / Nombre)",
        empty_label="-- Seleccione un usuario --",
        widget=forms.Select(attrs={'class': 'TxtCaja'})
    )
    codRol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label="Seleccionar Nuevo Rol",
        empty_label="-- Seleccione un rol --",
        widget=forms.Select(attrs={'class': 'TxtCaja'})
    )

# registro de productos
class ProductoForm(forms.ModelForm):
    unid_medida = forms.ChoiceField(
        choices=[
            ('Und', 'Unidades (Und)'),
            ('Kg', 'Kilogramos (Kg)'),
            ('L', 'Litros (L)'),
            ('Ml', 'Mililitros (Ml)'),
            ('Caja', 'Caja / Empaque'),
        ],
        label="Unidad de Medida",
        widget=forms.Select(attrs={'class': 'TxtCaja'})
    )
    precio_producto = forms.DecimalField(
        label="Precio de Venta ($)",
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'TxtCaja', 'placeholder': '0.00'})
    )
    fecha_vencimiento = forms.DateField(
        label="Fecha de Vencimiento Inicial",
        widget=forms.DateInput(attrs={'class': 'TxtCaja', 'type': 'date'})
    )
    lote = forms.CharField(
        required=False,
        label="Detalle / Lote Inicial",
        widget=forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Lote 2026-A'})
    )
    nuevo_grupo_nombre = forms.CharField(
        required=False,
        label="O Crear Nueva Categoría",
        widget=forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Vacunas, Alimentos...'})
    )

    class Meta:
        model = Productos
        fields = ['nombreproducto', 'descripcionproducto', 'fk_codgrupos']
        labels = {
            'nombreproducto': 'Nombre del Producto',
            'descripcionproducto': 'Descripción / Detalle',
            'fk_codgrupos': 'Categoría Existente',
        }
        widgets = {
            'nombreproducto': forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Amoxicilina 500mg'}),
            'descripcionproducto': forms.Textarea(attrs={'class': 'TxtCaja', 'rows': 3, 'placeholder': 'Descripción opcional del producto...'}),
            'fk_codgrupos': forms.Select(attrs={'class': 'TxtCaja'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fk_codgrupos'].required = False
        self.fields['fk_codgrupos'].empty_label = "-- Seleccionar existente --"

# ajustes manuales de inventario
class AjusteInventarioForm(forms.Form):
    TIPOS_AJUSTE = [
        ('carga', 'Carga (Entrada / Incremento de Stock)'),
        ('descarga', 'Descarga (Salida / Mermas / Detección)'),
    ]

    productoId = forms.ModelChoiceField(
        queryset=Productos.objects.all(),
        label="Seleccionar Producto",
        empty_label="-- Seleccione un producto --",
        widget=forms.Select(attrs={'class': 'TxtCaja'})
    )
    tipoAjuste = forms.ChoiceField(
        choices=TIPOS_AJUSTE,
        label="Tipo de Ajuste",
        widget=forms.Select(attrs={'class': 'TxtCaja'})
    )
    cantidadAjuste = forms.DecimalField(
        label="Cantidad a Ajustar",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: 10.00'})
    )
    costoAjuste = forms.DecimalField(
        required=False,
        label="Costo Unitario (Opcional)",
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'TxtCaja', 'placeholder': '0.00'})
    )
    detalleAjuste = forms.CharField(
        label="Motivo del Ajuste",
        widget=forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Inventario inicial, Producto dañado...'})
    )

# traslado de bodega o ubicacion
class TrasladoInventarioForm(forms.Form):
    productoId = forms.ModelChoiceField(
        queryset=Productos.objects.all(),
        label="Producto a Trasladar",
        empty_label="-- Seleccione un producto --",
        widget=forms.Select(attrs={'class': 'TxtCaja'})
    )
    ubicacionOrigen = forms.CharField(
        label="Ubicación Origen",
        widget=forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Bodega Principal'})
    )
    ubicacionDestino = forms.CharField(
        label="Ubicación Destino",
        widget=forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Vitrina 2 / Estante B'})
    )
    cantidadTraslado = forms.DecimalField(
        label="Cantidad a Trasladar",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'TxtCaja', 'placeholder': '0.00'})
    )
# crear proveedores
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        labels = {
            'nombreproveedor': 'Nombre / Razón Social del Proveedor',
            'nitproveedor': 'NIT o Documento',
            'emailproveedor': 'Correo Electrónico',
        }
        widgets = {
            'nombreproveedor': forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Distribuidora Veterinaria S.A.S.'}),
            'nitproveedor': forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: 900123456-1'}),
            'emailproveedor': forms.EmailInput(attrs={'class': 'TxtCaja', 'placeholder': 'contacto@proveedor.com'}),
        }
# datos cliente y tipo de pago en facturacion
class VentaHeaderForm(forms.Form):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta de Débito/Crédito', 'Tarjeta de Débito/Crédito'),
        ('Transferencia', 'Transferencia / Nequi'),
    ]

    numeroFactura = forms.CharField(
        label="N° Factura de Venta",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'TxtCaja', 
            'readonly': 'readonly',
            'style': 'background-color: #e9ecef; cursor: not-allowed;'
        })
    )
    clienteNombre = forms.CharField(
        label="Nombre del Cliente / Paciente",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: Juan Pérez'})
    )
    clienteCedula = forms.CharField(
        label="Cédula / Documento",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'TxtCaja', 'placeholder': 'Ej: 1088123456'})
    )
    metodoPago = forms.ChoiceField(
        choices=METODOS_PAGO,
        label="Método de Pago",
        widget=forms.Select(attrs={'class': 'TxtCaja'})
    )
# busqueda cliente
class ClienteBusquedaForm(forms.Form):
    busqueda = forms.CharField(
        required=False,
        label="Buscar por Nombre o Cédula",
        widget=forms.TextInput(attrs={
            'class': 'TxtCaja',
            'placeholder': 'Escriba un nombre o número de cédula...',
            'autofocus': 'autofocus'
        })
    )

# consultar producto 
class ConsultaProductoForm(forms.Form):
    busqueda = forms.CharField(
        required=False,
        label="Código de Barras / ID o Descripción",
        widget=forms.TextInput(attrs={
            'class': 'TxtCaja',
            'placeholder': 'Ej: 770123456789 o Amoxicilina...',
            'autofocus': 'autofocus'
        })
    )