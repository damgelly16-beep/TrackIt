from django.db import models

class Detalle(models.Model):
    coddetalle = models.AutoField(db_column='codDetalle', primary_key=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    valoriva = models.DecimalField(db_column='valorIva', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(db_column='subTotal', max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fk_codventa = models.ForeignKey('Ventas', models.DO_NOTHING, db_column='fk_codVenta')
    fk_codproducto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='fk_codProducto')

    class Meta:
        db_table = 'detalle'

class Grupo(models.Model):
    codgrupos = models.AutoField(db_column='codGrupos', primary_key=True)
    nombregrupos = models.CharField(db_column='nombreGrupos', max_length=50)

    class Meta:
        db_table = 'grupo'

class Inventario(models.Model):
    codinventario = models.AutoField(db_column='codInventario', primary_key=True)
    costosproductos = models.DecimalField(db_column='costosProductos', max_digits=10, decimal_places=2, blank=True, null=True)
    cantidadproducto = models.DecimalField(max_digits=10, decimal_places=2)
    unidmedida = models.CharField(db_column='unidMedida', max_length=10)
    lote = models.CharField(max_length=50, blank=True, null=True)
    precioproducto = models.DecimalField(db_column='precioProducto', max_digits=10, decimal_places=2)
    fechavenproducto = models.DateField(db_column='fechavenProducto')

    class Meta:
        db_table = 'inventario'

class Inventarioproducto(models.Model):
    codinvproducto = models.SmallAutoField(db_column='codinvProducto', primary_key=True)
    fk_codinventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='fk_codInventario')
    fk_codproducto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='fk_codProducto')

    class Meta:
        db_table = 'inventarioproducto'

class Productoproveedor(models.Model):
    codpproveedor = models.AutoField(db_column='codPproveedor', primary_key=True)
    fk_nitproveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='fk_nitProveedor')
    fk_codproducto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='fk_codProducto')

    class Meta:
        db_table = 'productoproveedor'

class Productos(models.Model):
    codproducto = models.AutoField(db_column='codProducto', primary_key=True)
    nombreproducto = models.CharField(db_column='nombreProducto', max_length=100)
    descripcionproducto = models.CharField(db_column='descripcionProducto', max_length=255)
    fk_codgrupos = models.ForeignKey(Grupo, models.DO_NOTHING, db_column='fk_codGrupos')

    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombreproducto
    
class Proveedor(models.Model):
    nitproveedor = models.CharField(db_column='nitProveedor', primary_key=True, max_length=20)
    nombreproveedor = models.CharField(db_column='nombreProveedor', max_length=100)
    direccionproveedor = models.CharField(db_column='direccionProveedor', max_length=150)
    telefonoproveedor = models.CharField(db_column='telefonoProveedor', max_length=20)
    emailproveedor = models.CharField(db_column='emailProveedor', max_length=100)

    class Meta:
        db_table = 'proveedor'

class Rol(models.Model):
    codrol = models.CharField(db_column='codRol', primary_key=True, max_length=10)
    nombrerol = models.CharField(db_column='nombreRol', max_length=50)

    class Meta:
        db_table = 'rol'

    def __str__(self):
        return self.nombrerol

class Ubicacion(models.Model):
    codubicacion = models.CharField(db_column='codUbicacion', primary_key=True, max_length=20)
    nombreubicacion = models.CharField(db_column='nombreUbicacion', max_length=100)
    fk_codinventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='fk_codInventario')

    class Meta:
        db_table = 'ubicacion'

class Usuario(models.Model):
    tipodocumento = models.CharField(db_column='tipoDocumento', max_length=3)
    numcedula = models.CharField(db_column='numCedula', primary_key=True, max_length=20)
    nombreusuario1 = models.CharField(db_column='nombreUsuario1', max_length=50)
    nombreusuario2 = models.CharField(db_column='nombreUsuario2', max_length=50, blank=True, null=True)
    apellidousuario1 = models.CharField(db_column='apellidoUsuario1', max_length=50)
    apellidousuario2 = models.CharField(db_column='apellidoUsuario2', max_length=50, blank=True, null=True)
    direccionusuario = models.CharField(db_column='direccionUsuario', max_length=150)
    departamento = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    telefonousuario = models.CharField(db_column='telefonoUsuario', max_length=20, blank=True, null=True)
    emailusuario = models.CharField(db_column='emailUsuario', max_length=100)
    fk_codrol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='fk_codRol')

    class Meta:
        db_table = 'usuario'

class Ventas(models.Model):
    codventa = models.AutoField(db_column='codVenta', primary_key=True)
    fechaventa = models.DateTimeField(db_column='fechaVenta')
    fk_numcedula = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='fk_numCedula')

    class Meta:
        db_table = 'ventas'