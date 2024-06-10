"""proyectois URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from seguridadApp.views.views import acceder, home, salir, perfil
from ventasApp.views.views import dashboard

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Api docs",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.minenick.pe",
        contact=openapi.Contact(email="nvegas@unitru.edu.pe"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('', acceder, name='login'),
    path('home/', home, name='home'),
    path('logout/', salir, name="logout"),

    path('perfil/', perfil, name="perfil"),
    path('usuario/', include('seguridadApp.routes.usuario'), name="usuario"),
    path('permiso/', include('seguridadApp.routes.permiso'), name="permiso"),
    path('role/', include('seguridadApp.routes.role'), name="role"),

    path('admin/', admin.site.urls, name="admin"),

    path('categoria/', include('ventasApp.routes.categoria'), name="categoria"),
    path('cliente/', include('ventasApp.routes.cliente'), name="cliente"),
    path('formaPago/', include('ventasApp.routes.formaPago'), name="formaPago"),
    path('producto/', include('ventasApp.routes.producto'), name="producto"),
    path('proveedor/', include('ventasApp.routes.proveedor'), name="proveedor"),
    path('tipoCliente/', include('ventasApp.routes.tipoCliente'), name="tipoCliente"),
    path('trabajador/', include('ventasApp.routes.trabajador'), name="trabajador"),
    path('pedidoVenta/', include('ventasApp.routes.pedidoVenta'), name="pedidoVenta"),
    path('ordenCompra/', include('ventasApp.routes.ordenCompra'), name="ordenCompra"),
    path('notaAlmacen/', include('ventasApp.routes.notaAlmacen'), name="notaAlmacen"),

    path('dashboard/', dashboard, name="dashboard"),
    path('api/', include('ventasApp.routes.api'), name="api"),
    path('api/', include('api.api.urls'), name="api2"),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
