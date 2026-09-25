# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Detalle(models.Model):
    coddetalle = models.AutoField(db_column='codDetalle', primary_key=True)  # Field name made lowercase.
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    valoriva = models.DecimalField(db_column='valorIva', max_digits=10, decimal_places=2)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='subTotal', max_digits=10, decimal_places=2)  # Field name made lowercase.
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fk_codventa = models.ForeignKey('Ventas', models.DO_NOTHING, db_column='fk_codVenta')  # Field name made lowercase.
    fk_codproducto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='fk_codProducto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalle'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Grupo(models.Model):
    codgrupos = models.AutoField(db_column='codGrupos', primary_key=True)  # Field name made lowercase.
    nombregrupos = models.CharField(db_column='nombreGrupos', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'grupo'


class Inventario(models.Model):
    codinventario = models.AutoField(db_column='codInventario', primary_key=True)  # Field name made lowercase.
    costosproductos = models.DecimalField(db_column='costosProductos', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cantidadproducto = models.DecimalField(max_digits=10, decimal_places=2)
    unidmedida = models.CharField(db_column='unidMedida', max_length=10)  # Field name made lowercase.
    lote = models.CharField(max_length=50, blank=True, null=True)
    precioproducto = models.DecimalField(db_column='precioProducto', max_digits=10, decimal_places=2)  # Field name made lowercase.
    fechavenproducto = models.DateField(db_column='fechavenProducto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inventario'


class Inventarioproducto(models.Model):
    codinvproducto = models.SmallAutoField(db_column='codinvProducto', primary_key=True)  # Field name made lowercase.
    fk_codinventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='fk_codInventario')  # Field name made lowercase.
    fk_codproducto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='fk_codProducto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inventarioproducto'


class Productoproveedor(models.Model):
    codpproveedor = models.AutoField(db_column='codPproveedor', primary_key=True)  # Field name made lowercase.
    fk_nitproveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='fk_nitProveedor')  # Field name made lowercase.
    fk_codproducto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='fk_codProducto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productoproveedor'


class Productos(models.Model):
    codproducto = models.AutoField(db_column='codProducto', primary_key=True)  # Field name made lowercase.
    nombreproducto = models.CharField(db_column='nombreProducto', max_length=100)  # Field name made lowercase.
    descripcionproducto = models.CharField(db_column='descripcionProducto', max_length=255)  # Field name made lowercase.
    fk_codgrupos = models.ForeignKey(Grupo, models.DO_NOTHING, db_column='fk_codGrupos')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productos'


class Proveedor(models.Model):
    nitproveedor = models.CharField(db_column='nitProveedor', primary_key=True, max_length=20)  # Field name made lowercase.
    nombreproveedor = models.CharField(db_column='nombreProveedor', max_length=100)  # Field name made lowercase.
    direccionproveedor = models.CharField(db_column='direccionProveedor', max_length=150)  # Field name made lowercase.
    telefonoproveedor = models.CharField(db_column='telefonoProveedor', max_length=20)  # Field name made lowercase.
    emailproveedor = models.CharField(db_column='emailProveedor', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'proveedor'


class Rol(models.Model):
    codrol = models.CharField(db_column='codRol', primary_key=True, max_length=10)  # Field name made lowercase.
    nombrerol = models.CharField(db_column='nombreRol', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rol'

    def __str__(self):
        return self.nombrerol

class Ubicacion(models.Model):
    codubicacion = models.CharField(db_column='codUbicacion', primary_key=True, max_length=20)  # Field name made lowercase.
    nombreubicacion = models.CharField(db_column='nombreUbicacion', max_length=100)  # Field name made lowercase.
    fk_codinventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='fk_codInventario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ubicacion'


class Usuario(models.Model):
    tipodocumento = models.CharField(db_column='tipoDocumento', max_length=3)  # Field name made lowercase.
    numcedula = models.CharField(db_column='numCedula', primary_key=True, max_length=20)  # Field name made lowercase.
    nombreusuario1 = models.CharField(db_column='nombreUsuario1', max_length=50)  # Field name made lowercase.
    nombreusuario2 = models.CharField(db_column='nombreUsuario2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    apellidousuario1 = models.CharField(db_column='apellidoUsuario1', max_length=50)  # Field name made lowercase.
    apellidousuario2 = models.CharField(db_column='apellidoUsuario2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    direccionusuario = models.CharField(db_column='direccionUsuario', max_length=150)  # Field name made lowercase.
    departamento = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    telefonousuario = models.CharField(db_column='telefonoUsuario', max_length=20, blank=True, null=True)  # Field name made lowercase.
    emailusuario = models.CharField(db_column='emailUsuario', max_length=100)  # Field name made lowercase.
    fk_codrol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='fk_codRol')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'


class Ventas(models.Model):
    codventa = models.AutoField(db_column='codVenta', primary_key=True)  # Field name made lowercase.
    fechaventa = models.DateTimeField(db_column='fechaVenta')  # Field name made lowercase.
    fk_numcedula = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='fk_numCedula')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ventas'
