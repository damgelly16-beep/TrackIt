from django.urls import path
from . import views

urlpatterns = [

    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),


    path('administracion/', views.admin_module_view, name='administracion'),
    path('administracion/registro/', views.registro_usuario_view, name='registro_usuario'),
    path('administracion/usuarios/', views.lista_usuarios_view, name='lista_usuarios'),
    path('administracion/usuarios/editar/<str:cedula>/', views.editar_usuario_view, name='editar_usuario'),
    path('administracion/asignar-permisos/', views.asignar_permisos_view, name='asignar_permisos'),
   
    path('inventario/', views.inventario_module_view, name='inventario_modulo'),
    path('inventario/producto/nuevo/', views.registrar_producto_view, name='registrar_producto'),
    path('inventario/ajuste/', views.registrar_inventario_view, name='registrar_inventario'),
    path('inventario/traslado/', views.registrar_traslado_inventario_view, name='registrar_traslado'),
    path('inventario/consultar/', views.consultar_producto_view, name='consultar_producto'),
    
    path('compras/', views.compras_module_view, name='compras_modulo'),
    path('compras/entrada/', views.entrada_mercancia_view, name='entrada_mercancia'),
    path('compras/proveedores/', views.gestion_proveedores_view, name='gestion_proveedores'),
    path('compras/historial/', views.historial_compras_view, name='historial_compras'),
   
    path('ventas/', views.ventas_modulo_view, name='ventas_modulo'),
    path('ventas/facturar/', views.registrar_venta_view, name='registrar_venta'),
    path('ventas/clientes/', views.directorio_clientes_view, name='directorio_clientes'),
    path('ventas/reporte/', views.reporte_ventas_view, name='reporte_ventas'),
   
    path('reportes/', views.reportes_general_view, name='reportes_general'),
]