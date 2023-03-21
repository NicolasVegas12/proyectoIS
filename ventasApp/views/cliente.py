from pydoc import describe
from django.shortcuts import render,redirect 
from ventasApp.models import Cliente, TipoCliente 
from django.db.models import Q 
from ventasApp.forms import ClienteForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import datetime
from ventasApp.decorators import group_required
from django.contrib.auth.decorators import login_required
# Create your views here.



def agregarcliente(request):
  
    if request.method=="POST":
        form=ClienteForm(request.POST)
        
        if form.is_valid():

            documentoIdentidad_cliente = form.cleaned_data.get("documentoIdentidad")
            cliente_exits = (Cliente.objects.filter(documentoIdentidad=documentoIdentidad_cliente).count()>0)
            if cliente_exits:
                messages.info(request, "Cliente ya existe.")            
                form=ClienteForm()
                form.fields["tipoCliente"].choices = [(r['idTipoCliente'],r['descripcion']) for r in TipoCliente.objects.exclude(eliminado=1).values()]
                context={'form':form}
                return render(request,"cliente/agregar.html",context) 
            else:
                messages.success(request, "Cliente registrada.")
                form.save() 
                element = Cliente.objects.all().last()
                element.usuarioRegistro =  request.session['user_logged']
                element.save()
                return redirect("listarcliente") 

    else:
        form=ClienteForm() 
            
        form.fields["tipoCliente"].choices = [(r['idTipoCliente'],r['descripcion']) for r in TipoCliente.objects.exclude(eliminado=1).values()]
        
        context={'form':form} 
        return render(request,"cliente/agregar.html",context) 
    


def listarcliente(request):
    
    queryset = request.GET.get("buscar")
    cliente = Cliente.objects.all().filter(eliminado=False).order_by('idCliente').values()
    if queryset:
        cliente=Cliente.objects.filter(Q(documentoIdentidad__icontains=queryset)).filter(eliminado=False).distinct().order_by('idCliente').values() 
    list_cliente = []
    for c in cliente:
        tipo_cliente=TipoCliente.objects.get(idTipoCliente=c['tipoCliente_id'])
        list_cliente.append({
            'idCliente': c['idCliente'], 'tipoCliente': tipo_cliente, 'nombres': c['nombres'], 'apellidos': c['apellidos'], 'direccion': c['direccion'], 'email': c['email'], 'telefono': c['telefono'], 'tipoDocumentoIdentidad': c['tipoDocumentoIdentidad'], 'documentoIdentidad': c['documentoIdentidad'], 'activo': c['activo'], 'eliminado': c['eliminado'], 'usuarioRegistro': c['usuarioRegistro'], 'fechaRegistro': c['fechaRegistro'], 'usuarioModificacion': c['usuarioModificacion'], 'fechaModificacion': c['fechaModificacion'], 'usuarioEliminacion': c['usuarioEliminacion'], 'fechaEliminacion': c['fechaEliminacion']
        })
    paginator = Paginator(list_cliente, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"cliente/listar.html",{'page_obj': page_obj})



def editarcliente(request,id):
    cliente=Cliente.objects.get(idCliente=id)
    if request.method=="POST":
        form=ClienteForm(request.POST,instance=cliente)
        form.fields["tipoCliente"].choices = [(r['idTipoCliente'],r['descripcion']) for r in TipoCliente.objects.exclude(eliminado=1).values()]
        if form.is_valid():
            messages.success(request, "Cliente actualizado.")
            form.save() 
            elemento = Cliente.objects.get(idCliente=id)
            elemento.usuarioModificacion = request.session['user_logged']
            elemento.fechaModificacion = datetime.datetime.now()
            elemento.save()
            return redirect("listarcliente") 
    else:
        form=ClienteForm(instance=cliente)
        form.fields["tipoCliente"].choices = [(r['idTipoCliente'],r['descripcion']) for r in TipoCliente.objects.exclude(eliminado=1).values()]
        
        context={"form":form} 
        return render(request,"cliente/edit.html",context)



def eliminarcliente(request,id):
    cliente=Cliente.objects.get(idCliente=id) 
    cliente.activo=False
    cliente.eliminado=True
    cliente.usuarioEliminacion = request.session['user_logged']
    cliente.fechaEliminacion = datetime.datetime.now()
    cliente.save()
    messages.success(request, "Cliente eliminado.")
    return redirect("listarcliente")

def activarcliente(request,id,activo):
    cliente=Cliente.objects.get(idCliente=id)
    if activo == 0:
        cliente.activo=True
    else:
        cliente.activo=False
    cliente.save()
    messages.success(request, "Cliente actualizado.")
    return redirect("listarcliente") 