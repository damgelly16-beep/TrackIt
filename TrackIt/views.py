import json
from datetime import datetime
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Q

# imports de modelos y formularios del proyecto
from .models import Usuario, Rol, Productos, Grupo, Inventario, Inventarioproducto, Proveedor
from .forms import (
    LoginForm, UsuarioForm, UsuarioEditarForm, AsignarPermisosForm,
    ProductoForm, AjusteInventarioForm, TrasladoInventarioForm, ProveedorForm,
    VentaHeaderForm, ClienteBusquedaForm, ConsultaProductoForm
)

# verificacion de inicio de sesion
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_logged'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# verificacion por rol de usuario
def rol_requerido(*rol):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.session.get('usuario_logged'):
                return redirect('login')
            user_rol = request.session.get('rol')
            if request.session.get('usuario_logged') != 'admin' and user_rol not in rol:
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def inicio(request):
    return render(request, 'index.html')

# autenticacion de usuario
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['TxtUsuario'].strip()
            password = form.cleaned_data['TxtPassword'].strip()

            # admin por defecto
            if usuario == 'admin' and password == '1234':
                request.session['usuario_logged'] = 'admin'
                request.session['rol'] = 'Administrador'
                messages.success(request, '¡Ingreso correcto como Administrador!')
                return redirect('dashboard')

            user_django = User.objects.filter(username=usuario).first()
            if user_django and user_django.check_password(password):
                request.session['usuario_logged'] = user_django.username
                
                try:
                    perfil = Usuario.objects.filter(Q(numcedula=user_django.username) | Q(emailusuario=user_django.email)).first()
                    if perfil and perfil.fk_codrol:
                        request.session['rol'] = perfil.fk_codrol.nombrerol
                    else:
                        request.session['rol'] = None
                except Exception:
                    request.session['rol'] = None

                messages.success(request, f'¡Bienvenido {user_django.first_name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, completa todos los campos correctamente.')
    else:
        form = LoginForm()
    return render(request, 'Login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

@login_required
def dashboard_view(request):
    rol_usuario = request.session.get('rol')
    return render(request, 'dashboard.html', {'rol_usuario': rol_usuario})

@login_required
@rol_requerido('Administrador')
def admin_module_view(request):
    total_usuarios = Usuario.objects.count()
    total_roles = Rol.objects.count()
    contexto = {'total_usuarios': total_usuarios, 'total_roles': total_roles}
    return render(request, 'administracion.html', contexto)

# registro de nuevos usuarios del sistema
@login_required
@rol_requerido('Administrador')
def registro_usuario_view(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        username = request.POST.get('username')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        elif form.is_valid():
            try:
                user_django = User.objects.create_user(
                    username=username,
                    email=form.cleaned_data['emailusuario'],
                    password=form.cleaned_data['numcedula'],
                    first_name=form.cleaned_data['nombreusuario1'],
                    last_name=form.cleaned_data['apellidousuario1']
                )
                form.save()
                messages.success(request, f'¡Usuario "{username}" creado exitosamente!')
                return redirect('administracion')
            except Exception as e:
                messages.error(request, f'Error al guardar usuario: {e}')
        else:
            messages.error(request, 'Por favor verifique los datos ingresados en el formulario.')
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form})

@login_required
@rol_requerido('Administrador')
def lista_usuarios_view(request):
    busqueda = request.GET.get('busqueda', '').strip()
    usuarios_list = Usuario.objects.all()

    if busqueda:
        usuarios_list = usuarios_list.filter(
            Q(numcedula__icontains=busqueda) |
            Q(nombreusuario1__icontains=busqueda) |
            Q(apellidousuario1__icontains=busqueda)
        )
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios_list, 'busqueda': busqueda})

@login_required
@rol_requerido('Administrador')
def editar_usuario_view(request, cedula):
    usuario_obj = get_object_or_404(Usuario, numcedula=cedula)

    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario_obj)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'¡Datos de {usuario_obj.nombreusuario1} actualizados correctamente!')
                return redirect('lista_usuarios')
            except Exception as e:
                messages.error(request, f'Error al actualizar usuario: {e}')
        else:
            messages.error(request, 'Por favor verifique los campos del formulario.')
    else:
        form = UsuarioEditarForm(instance=usuario_obj)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario_obj})

@login_required
@rol_requerido('Administrador')
def asignar_permisos_view(request):
    if request.method == 'POST':
        form = AsignarPermisosForm(request.POST)
        if form.is_valid():
            try:
                usuario_obj = form.cleaned_data['numCedula']
                rol_obj = form.cleaned_data['codRol']

                usuario_obj.fk_codrol = rol_obj
                usuario_obj.save()

                messages.success(request, f'¡Rol "{rol_obj.nombrerol}" asignado exitosamente a {usuario_obj.nombreusuario1}!')
                return redirect('administracion')
            except Exception as e:
                messages.error(request, f'Error al asignar el rol: {e}')
        else:
            messages.error(request, 'Por favor verifique las selecciones del formulario.')
    else:
        form = AsignarPermisosForm()
    return render(request, 'asignar_permisos.html', {'form': form})

@login_required
@rol_requerido('Administrador', 'Bodeguero', 'Veterinario')
def inventario_module_view(request):
    return render(request, 'inventario_modulo.html')

# crear producto nuevo en base de datos
@login_required
@rol_requerido('Administrador', 'Bodeguero', 'Veterinario')
def registrar_producto_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            try:
                nuevo_grupo = form.cleaned_data.get('nuevo_grupo_nombre')
                grupo_existente = form.cleaned_data.get('fk_codgrupos')

                if nuevo_grupo and nuevo_grupo.strip():
                    grupo_obj = Grupo.objects.create(nombregrupos=nuevo_grupo.strip())
                elif grupo_existente:
                    grupo_obj = grupo_existente
                else:
                    messages.error(request, 'Debe seleccionar o crear una categoría.')
                    return render(request, 'registrar_producto.html', {'form': form})

                producto = form.save(commit=False)
                producto.fk_codgrupos = grupo_obj
                producto.save()

                # inicia stock en cero
                nuevo_inventario = Inventario.objects.create(
                    costosproductos=None,
                    cantidadproducto=0,
                    unidmedida=form.cleaned_data['unid_medida'],
                    lote=form.cleaned_data.get('lote', ''),
                    precioproducto=form.cleaned_data['precio_producto'],
                    fechavenproducto=form.cleaned_data['fecha_vencimiento']
                )

                Inventarioproducto.objects.create(
                    fk_codinventario=nuevo_inventario,
                    fk_codproducto=producto
                )

                messages.success(request, '¡Producto registrado exitosamente!')
                return redirect('inventario_modulo')
            except Exception as e:
                messages.error(request, f'Error al registrar producto: {e}')
        else:
            messages.error(request, 'Por favor verifique los datos del formulario.')
    else:
        form = ProductoForm()
    return render(request, 'registrar_producto.html', {'form': form})

# ajustes manuales de stock
@login_required
@rol_requerido('Administrador', 'Bodeguero', 'Veterinario')
def registrar_inventario_view(request):
    if request.method == 'POST':
        form = AjusteInventarioForm(request.POST)
        if form.is_valid():
            try:
                producto_obj = form.cleaned_data['productoId']
                tipo_ajuste = form.cleaned_data['tipoAjuste']
                cantidad = float(form.cleaned_data['cantidadAjuste'])
                costo = form.cleaned_data['costoAjuste']
                motivo = form.cleaned_data['detalleAjuste']

                if tipo_ajuste == 'descarga':
                    cantidad_final = -cantidad
                else:
                    cantidad_final = cantidad

                lote_detalle = f"AJUSTE ({tipo_ajuste.upper()}): {motivo}"

                nuevo_inventario = Inventario.objects.create(
                    costosproductos=costo,
                    cantidadproducto=cantidad_final,
                    unidmedida='Und',
                    lote=lote_detalle,
                    precioproducto=0,
                    fechavenproducto='2026-12-31'
                )

                Inventarioproducto.objects.create(
                    fk_codinventario=nuevo_inventario,
                    fk_codproducto=producto_obj
                )

                messages.success(request, f'¡Ajuste de inventario para "{producto_obj.nombreproducto}" registrado exitosamente!')
                return redirect('inventario_modulo')
            except Exception as e:
                messages.error(request, f'Error al registrar ajuste: {e}')
        else:
            messages.error(request, 'Por favor verifique los datos ingresados en el formulario.')
    else:
        form = AjusteInventarioForm()
    return render(request, 'registrar_inventario.html', {'form': form})

@login_required
@rol_requerido('Administrador', 'Bodeguero')
def registrar_traslado_inventario_view(request):
    if request.method == 'POST':
        form = TrasladoInventarioForm(request.POST)
        if form.is_valid():
            try:
                producto_obj = form.cleaned_data['productoId']
                ubicacion_origen = form.cleaned_data['ubicacionOrigen'].strip()
                ubicacion_destino = form.cleaned_data['ubicacionDestino'].strip()
                cantidad = float(form.cleaned_data['cantidadTraslado'])

                nuevo_inventario_salida = Inventario.objects.create(
                    costosproductos=None,
                    cantidadproducto=-cantidad,
                    unidmedida='Und',
                    lote=f'TRASLADO: {ubicacion_origen} -> {ubicacion_destino}',
                    precioproducto=0,
                    fechavenproducto='2026-12-31'
                )

                Inventarioproducto.objects.create(
                    fk_codinventario=nuevo_inventario_salida,
                    fk_codproducto=producto_obj
                )

                messages.success(request, f'¡Traslado de {cantidad} unidades de "{producto_obj.nombreproducto}" registrado con éxito!')
                return redirect('inventario_modulo')
            except Exception as e:
                messages.error(request, f'Error al registrar el traslado: {e}')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            if not form.non_field_errors():
                messages.error(request, 'Por favor verifique los datos del formulario.')
    else:
        form = TrasladoInventarioForm()
    return render(request, 'registrar_traslado.html', {'form': form})

@login_required
@rol_requerido('Administrador', 'Bodeguero')
def compras_module_view(request):
    return render(request, 'compras_modulo.html')

# entrada por compra a proveedor
@login_required
@rol_requerido('Administrador', 'Bodeguero')
def entrada_mercancia_view(request):
    productos = Productos.objects.all()
    if request.method == 'POST':
        numero_factura = request.POST.get('numeroFactura', '').strip()
        proveedor_nombre = request.POST.get('proveedorNombre', '').strip()
        fecha_ingreso = request.POST.get('fechaIngreso')
        detalles_json = request.POST.get('detallesProductosJson', '[]')

        try:
            items = json.loads(detalles_json)
            if not items:
                messages.error(request, 'Debe agregar al menos un producto.')
                return render(request, 'entrada_mercancia.html', {'productos': productos})

            for item in items:
                prod_id = item.get('productoId')
                cant = float(item.get('cantidad', 0))
                costo = float(item.get('costo', 0))
                porcentaje_iva = float(item.get('iva', 0))

                lote_detalle = f'FAC: {numero_factura} | PROV: {proveedor_nombre} | IVA: {porcentaje_iva}%'

                nuevo_inventario = Inventario.objects.create(
                    costosproductos=costo,
                    cantidadproducto=cant,
                    unidmedida='Und',
                    lote=lote_detalle,
                    precioproducto=0,
                    fechavenproducto=fecha_ingreso if fecha_ingreso else '2026-12-31'
                )

                producto_obj = Productos.objects.get(pk=prod_id)
                Inventarioproducto.objects.create(
                    fk_codinventario=nuevo_inventario,
                    fk_codproducto=producto_obj
                )

            messages.success(request, f'¡Factura {numero_factura} guardada!')
            return redirect('compras_modulo')
        except Exception as e:
            messages.error(request, f'Error al registrar entrada: {e}')

    return render(request, 'entrada_mercancia.html', {'productos': productos})

@login_required
@rol_requerido('Administrador', 'Bodeguero')
def gestion_proveedores_view(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            try:
                proveedor = form.save()
                messages.success(request, f'¡Proveedor "{proveedor.nombreproveedor}" (NIT: {proveedor.nitproveedor}) registrado exitosamente!')
                return redirect('compras_modulo')
            except Exception as e:
                messages.error(request, f'Error al guardar en la base de datos: {e}')
        else:
            messages.error(request, 'Por favor verifique los datos ingresados en el formulario.')
    else:
        form = ProveedorForm()
    return render(request, 'gestion_proveedores.html', {'form': form})

# historial de compras excluyendo ventas
@login_required
@rol_requerido('Administrador', 'Bodeguero')
def historial_compras_view(request):
    busqueda_proveedor = request.GET.get('busquedaProveedor', '').strip()
    busqueda_producto = request.GET.get('busquedaProducto', '').strip()

    registros = Inventario.objects.filter(lote__icontains='FAC:').exclude(lote__icontains='VENTA')

    if busqueda_proveedor:
        registros = registros.filter(lote__icontains=f'PROV: {busqueda_proveedor}')

    if busqueda_producto:
        registros = registros.filter(lote__icontains=busqueda_producto)

    historial = []
    for reg in registros:
        lote_texto = reg.lote or ''
        num_doc = 'N/A'
        proveedor = 'N/A'

        if 'FAC:' in lote_texto:
            partes = lote_texto.split('|')
            for parte in partes:
                if 'FAC:' in parte and 'VENTA' not in parte:
                    num_doc = parte.replace('FAC:', '').strip()
                elif 'PROV:' in parte:
                    proveedor = parte.replace('PROV:', '').strip()

        pivote = Inventarioproducto.objects.filter(fk_codinventario=reg).first()
        if pivote and pivote.fk_codproducto:
            nombre_prod = pivote.fk_codproducto.nombreproducto
        else:
            nombre_prod = 'Producto'

        historial.append({
            'num_documento': num_doc,
            'proveedor': proveedor,
            'producto': nombre_prod,
            'fecha': reg.fechavenproducto,
            'cantidad': reg.cantidadproducto,
            'costo': reg.costosproductos
        })

    return render(request, 'historial_compras.html', {
        'historial': historial,
        'busqueda_proveedor': busqueda_proveedor,
        'busqueda_producto': busqueda_producto
    })

@login_required
@rol_requerido('Administrador', 'Cajero', 'Veterinario')
def ventas_modulo_view(request):
    return render(request, 'ventas_modulo.html')

# registro de ventas y facturacion
@login_required
@rol_requerido('Administrador', 'Cajero', 'Veterinario')
def registrar_venta_view(request):
    ultimo_registro = Inventario.objects.filter(lote__icontains='VENTA FAC: VTA-').last()
    siguiente_numero = 1

    if ultimo_registro and ultimo_registro.lote:
        try:
            parte_fac = ultimo_registro.lote.split('VENTA FAC:')[1].split('|')[0].strip()
            num_str = parte_fac.replace('VTA-', '').strip()
            siguiente_numero = int(num_str) + 1
        except Exception:
            siguiente_numero = 1

    num_factura_autogenerado = f"VTA-{siguiente_numero:04d}"

    productos_db = Productos.objects.all()
    lista_productos = []

    for prod in productos_db:
        inv_pivotes = Inventarioproducto.objects.filter(fk_codproducto=prod)
        ids_inv = inv_pivotes.values_list('fk_codinventario_id', flat=True)
        movimientos = Inventario.objects.filter(codinventario__in=ids_inv)
        
        stock_actual = movimientos.aggregate(Sum('cantidadproducto'))['cantidadproducto__sum'] or 0
        ultimo_mov = movimientos.last()
        
        if ultimo_mov and ultimo_mov.precioproducto:
            precio_sugerido = ultimo_mov.precioproducto
        else:
            precio_sugerido = 0

        lista_productos.append({
            'pk': str(prod.pk),
            'nombreproducto': prod.nombreproducto,
            'precio': float(precio_sugerido),
            'stock': stock_actual
        })

    if request.method == 'POST':
        data_post = request.POST.copy()
        data_post['numeroFactura'] = num_factura_autogenerado
        
        form = VentaHeaderForm(data_post)
        detalles_json = request.POST.get('detallesProductosJson', '[]')

        if form.is_valid():
            try:
                items = json.loads(detalles_json)
                if not items:
                    messages.error(request, 'Debe agregar al menos un producto a la factura.')
                    return render(request, 'registrar_venta.html', {
                        'form': form, 
                        'productos': lista_productos,
                        'num_factura_autogenerado': num_factura_autogenerado
                    })

                num_factura = num_factura_autogenerado
                cliente_nombre = form.cleaned_data['clienteNombre'].strip()
                cliente_cedula = form.cleaned_data['clienteCedula'].strip()
                metodo_pago = form.cleaned_data['metodoPago']

                for item in items:
                    prod_id = item.get('productoId')
                    cant = float(item.get('cantidad', 0))
                    precio = float(item.get('precio', 0))

                    lote_detalle = f'VENTA FAC: {num_factura} | CLIENTE: {cliente_nombre} ({cliente_cedula}) | PAGO: {metodo_pago}'

                    nuevo_inventario = Inventario.objects.create(
                        costosproductos=None,
                        cantidadproducto=-cant,
                        unidmedida='Und',
                        lote=lote_detalle,
                        precioproducto=precio,
                        fechavenproducto='2026-12-31'
                    )

                    producto_obj = Productos.objects.get(pk=prod_id)
                    Inventarioproducto.objects.create(
                        fk_codinventario=nuevo_inventario,
                        fk_codproducto=producto_obj
                    )

                messages.success(request, f'¡Factura N° {num_factura} emitida correctamente!')
                return redirect('ventas_modulo')
            except Exception as e:
                messages.error(request, f'Error al registrar la venta: {e}')
        else:
            messages.error(request, 'Por favor verifique los datos de la factura.')
    else:
        form = VentaHeaderForm(initial={'numeroFactura': num_factura_autogenerado})

    return render(request, 'registrar_venta.html', {
        'form': form, 
        'productos': lista_productos,
        'num_factura_autogenerado': num_factura_autogenerado
    })

@login_required
@rol_requerido('Administrador', 'Cajero', 'Veterinario')
def directorio_clientes_view(request):
    form = ClienteBusquedaForm(request.GET)
    busqueda = ''
    if form.is_valid():
        busqueda = form.cleaned_data.get('busqueda', '').strip().lower()

    registros = Inventario.objects.filter(lote__icontains='VENTA FAC:')
    clientes_dict = {}

    for reg in registros:
        lote_texto = reg.lote or ''
        if 'CLIENTE:' in lote_texto:
            try:
                parte_cliente = lote_texto.split('CLIENTE:')[1].split('|')[0].strip()
                if '(' in parte_cliente and ')' in parte_cliente:
                    nombre = parte_cliente.split('(')[0].strip()
                    cedula = parte_cliente.split('(')[1].replace(')', '').strip()
                else:
                    nombre = parte_cliente
                    cedula = 'N/A'

                metodo_pago = 'N/A'
                if 'PAGO:' in lote_texto:
                    metodo_pago = lote_texto.split('PAGO:')[1].strip()

                if cedula not in clientes_dict:
                    clientes_dict[cedula] = {
                        'nombre': nombre,
                        'cedula': cedula,
                        'ultimo_pago': metodo_pago,
                        'total_compras': 1
                    }
                else:
                    clientes_dict[cedula]['total_compras'] += 1
            except Exception:
                continue

    lista_clientes = list(clientes_dict.values())
    if busqueda:
        lista_clientes = [
            c for c in lista_clientes
            if busqueda in c['nombre'].lower() or busqueda in c['cedula'].lower()
        ]

    return render(request, 'directorio_clientes.html', {'form': form, 'clientes': lista_clientes})

# cierre diario de caja
@login_required
@rol_requerido('Administrador', 'Cajero')
def reporte_ventas_view(request):
    tipo_cierre = request.GET.get('tipoCierre', 'diario')
    fecha_filtro = request.GET.get('fechaFiltro', datetime.now().strftime('%Y-%m-%d'))

    registros = Inventario.objects.filter(lote__icontains='VENTA FAC:')

    total_recaudado = 0.0
    total_unidades = 0.0
    facturas_procesadas = set()
    metodos_pago = {'Efectivo': 0.0, 'Tarjeta de Débito/Crédito': 0.0, 'Transferencia': 0.0}
    ventas_detalle = []

    for reg in registros:
        lote_texto = reg.lote or ''
        num_factura = 'N/A'
        cliente = 'N/A'
        pago = 'Efectivo'

        if 'VENTA FAC:' in lote_texto:
            partes = lote_texto.split('|')
            for parte in partes:
                if 'VENTA FAC:' in parte:
                    num_factura = parte.replace('VENTA FAC:', '').strip()
                elif 'CLIENTE:' in parte:
                    cliente = parte.replace('CLIENTE:', '').strip()
                elif 'PAGO:' in parte:
                    pago = parte.replace('PAGO:', '').strip()

        fecha_reg_str = str(reg.fechavenproducto)
        if fecha_filtro and (fecha_filtro not in fecha_reg_str):
            continue

        cant = abs(float(reg.cantidadproducto or 0))
        precio = float(reg.precioproducto or 0)
        subtotal = cant * precio

        total_recaudado += subtotal
        total_unidades += cant
        if num_factura != 'N/A':
            facturas_procesadas.add(num_factura)

        if pago in metodos_pago:
            metodos_pago[pago] += subtotal
        else:
            metodos_pago[pago] = subtotal

        pivote = Inventarioproducto.objects.filter(fk_codinventario=reg).first()
        if pivote and pivote.fk_codproducto:
            nombre_prod = pivote.fk_codproducto.nombreproducto
        else:
            nombre_prod = 'Producto'

        ventas_detalle.append({
            'factura': num_factura,
            'cliente': cliente,
            'producto': nombre_prod,
            'metodo_pago': pago,
            'cantidad': cant,
            'precio_unitario': precio,
            'total': subtotal
        })

    return render(request, 'reporte_ventas.html', {
        'tipo_cierre': tipo_cierre,
        'fecha_filtro': fecha_filtro,
        'total_recaudado': total_recaudado,
        'total_unidades': total_unidades,
        'total_facturas': len(facturas_procesadas),
        'metodos_pago': metodos_pago,
        'ventas_detalle': ventas_detalle
    })

# reportes globales
@login_required
@rol_requerido('Administrador')
def reportes_general_view(request):
    tipo_reporte = request.GET.get('tipo', 'inventario')

    reporte_inventario = []
    total_unidades_inv = 0
    total_costo_inv = 0
    total_valor_venta_inv = 0

    if tipo_reporte == 'inventario':
        productos = Productos.objects.all()
        for prod in productos:
            inv_pivotes = Inventarioproducto.objects.filter(fk_codproducto=prod)
            ids_inv = inv_pivotes.values_list('fk_codinventario_id', flat=True)
            movimientos = Inventario.objects.filter(codinventario__in=ids_inv)

            stock_actual = movimientos.aggregate(Sum('cantidadproducto'))['cantidadproducto__sum'] or 0
            ultimo_mov = movimientos.last()
            
            if ultimo_mov and ultimo_mov.costosproductos:
                costo_unit = ultimo_mov.costosproductos
            else:
                costo_unit = 0

            if ultimo_mov and ultimo_mov.precioproducto:
                precio_unit = ultimo_mov.precioproducto
            else:
                precio_unit = 0

            costo_total = stock_actual * costo_unit
            valor_venta_total = stock_actual * precio_unit

            total_unidades_inv += stock_actual
            total_costo_inv += costo_total
            total_valor_venta_inv += valor_venta_total

            reporte_inventario.append({
                'producto': prod.nombreproducto,
                'categoria': prod.fk_codgrupos.nombregrupos if prod.fk_codgrupos else 'Sin categoría',
                'stock': stock_actual,
                'costo_unitario': costo_unit,
                'costo_total': costo_total,
                'precio_venta': precio_unit,
                'valor_venta_total': valor_venta_total
            })

    reporte_movimientos = []
    if tipo_reporte == 'movimientos':
        registros = Inventario.objects.all().order_by('-codinventario')
        for reg in registros:
            pivote = Inventarioproducto.objects.filter(fk_codinventario=reg).first()
            if pivote and pivote.fk_codproducto:
                nombre_prod = pivote.fk_codproducto.nombreproducto
            else:
                nombre_prod = 'Desconocido'

            reporte_movimientos.append({
                'id': reg.codinventario,
                'producto': nombre_prod,
                'cantidad': reg.cantidadproducto,
                'detalle_lote': reg.lote or 'Sin detalle',
                'fecha_vencimiento': reg.fechavenproducto
            })

    reporte_compras = []
    total_compras_dinero = 0
    if tipo_reporte == 'compras':
        registros_compras = Inventario.objects.filter(lote__icontains='FAC:')
        compras_dict = {}

        for reg in registros_compras:
            lote_texto = reg.lote or ''
            proveedor = 'Proveedor Desconocido'
            num_fac = 'N/A'

            if '|' in lote_texto:
                partes = lote_texto.split('|')
                for parte in partes:
                    if 'PROV:' in parte:
                        proveedor = parte.replace('PROV:', '').strip()
                    elif 'FAC:' in parte:
                        num_fac = parte.replace('FAC:', '').strip()

            cant = reg.cantidadproducto or 0
            costo = reg.costosproductos or 0
            subtotal = cant * costo

            if proveedor not in compras_dict:
                compras_dict[proveedor] = {
                    'proveedor': proveedor,
                    'total_facturas': set([num_fac]),
                    'total_unidades': cant,
                    'total_gasto': subtotal
                }
            else:
                compras_dict[proveedor]['total_facturas'].add(num_fac)
                compras_dict[proveedor]['total_unidades'] += cant
                compras_dict[proveedor]['total_gasto'] += subtotal

            total_compras_dinero += subtotal

        for item in compras_dict.values():
            item['total_facturas'] = len(item['total_facturas'])
            reporte_compras.append(item)

    reporte_ventas = []
    total_ventas_dinero = 0
    if tipo_reporte == 'ventas':
        registros_ventas = Inventario.objects.filter(lote__icontains='VENTA FAC:')
        for reg in registros_ventas:
            lote_texto = reg.lote or ''
            num_fac = 'N/A'
            cliente = 'N/A'
            pago = 'Otro'

            partes = lote_texto.split('|')
            for parte in partes:
                if 'VENTA FAC:' in parte:
                    num_fac = parte.replace('VENTA FAC:', '').strip()
                elif 'CLIENTE:' in parte:
                    cliente = parte.replace('CLIENTE:', '').strip()
                elif 'PAGO:' in parte:
                    pago = parte.replace('PAGO:', '').strip()

            cant = abs(reg.cantidadproducto or 0)
            precio = reg.precioproducto or 0
            subtotal = cant * precio
            total_ventas_dinero += subtotal

            reporte_ventas.append({
                'factura': num_fac,
                'cliente': cliente,
                'metodo_pago': pago,
                'cantidad': cant,
                'precio_unitario': precio,
                'total': subtotal
            })

    return render(request, 'reportes.html', {
        'tipo_reporte': tipo_reporte,
        'reporte_inventario': reporte_inventario,
        'total_unidades_inv': total_unidades_inv,
        'total_costo_inv': total_costo_inv,
        'total_valor_venta_inv': total_valor_venta_inv,
        'reporte_movimientos': reporte_movimientos,
        'reporte_compras': reporte_compras,
        'total_compras_dinero': total_compras_dinero,
        'reporte_ventas': reporte_ventas,
        'total_ventas_dinero': total_ventas_dinero
    })

# consulta de existencias por codigo o nombre
@login_required
@rol_requerido('Administrador', 'Bodeguero', 'Veterinario', 'Cajero')
def consultar_producto_view(request):
    form = ConsultaProductoForm(request.GET)
    busqueda = ''
    producto_info = None

    if form.is_valid():
        busqueda = form.cleaned_data.get('busqueda', '').strip()

    if busqueda:
        producto = Productos.objects.filter(
            Q(pk__iexact=busqueda) | 
            Q(nombreproducto__icontains=busqueda) | 
            Q(descripcionproducto__icontains=busqueda)
        ).first()

        if producto:
            inv_pivotes = Inventarioproducto.objects.filter(fk_codproducto=producto)
            ids_inv = inv_pivotes.values_list('fk_codinventario_id', flat=True)
            movimientos = Inventario.objects.filter(codinventario__in=ids_inv).order_by('-codinventario')

            stock_total = movimientos.aggregate(Sum('cantidadproducto'))['cantidadproducto__sum'] or 0
            ultimo_mov = movimientos.last()
            
            if ultimo_mov and ultimo_mov.precioproducto:
                precio = ultimo_mov.precioproducto
            else:
                precio = 0

            if ultimo_mov and ultimo_mov.costosproductos:
                costo = ultimo_mov.costosproductos
            else:
                costo = 0

            if ultimo_mov and ultimo_mov.lote:
                lote = ultimo_mov.lote
            else:
                lote = 'N/A'

            if ultimo_mov and ultimo_mov.fechavenproducto:
                fechaven = ultimo_mov.fechavenproducto
            else:
                fechaven = 'N/A'

            producto_info = {
                'producto': producto,
                'stock_total': stock_total,
                'precio_venta': precio,
                'costo': costo,
                'lote': lote,
                'fecha_vencimiento': fechaven,
                'categoria': producto.fk_codgrupos.nombregrupos if producto.fk_codgrupos else 'Sin categoría',
                'movimientos': movimientos[:10]
            }
        else:
            messages.warning(request, f'No se encontró ningún producto con el criterio: "{busqueda}".')

    return render(request, 'consulta_producto.html', {
        'form': form,
        'producto_info': producto_info,
        'busqueda': busqueda
    })