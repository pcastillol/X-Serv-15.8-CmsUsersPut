from django.shortcuts import render
from .models import Pages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

FORMULARIO = """
    <form action="" method="POST">
        Nombre: <input type="text" name="nombre" value="Real Madrid"><br>
        Pagina: <input type="text" name="pagina" value="12 Champions"><br>
        <input type="submit" value="Enviar">
    </form>
"""

def barra(request):
    if request.user.is_authenticated():
        logged = "Logged in as " + request.user.username + ". <a href='/logout'>Logout</a>"
    else:
        logged = "Not logged in. <a href='/login'>Login</a>"

    pages = Pages.objects.all()
    respuesta = "<br><br><h1>Bienvenido a tu CMS.</h1>"

    if len(pages)==0:
        respuesta += "Aún no hay contenidos almacenados.<br>"
    else:
        respuesta += "Estos son los contenidos almacenados:<br>"

    respuesta += "<ul>"
    for page in pages:
        respuesta += "<li><a href='/content/" + str(page.id) + "'>" + page.name + "</a>"
    respuesta += "</ul>"
    return HttpResponse(logged + respuesta)

@csrf_exempt
def content(request, num):
    if request.method == "POST":
        pagina = Pages(name = request.POST['nombre'], page = request.POST['pagina'])
        pagina.save()
        #num = str(pagina.id)
        return HttpResponseRedirect("/content/" + str(pagina.id))
    try:
        pagina = Pages.objects.get(id=int(num))
    except Pages.DoesNotExist:
        respuesta = "No existe"
        if request.user.is_authenticated():
            respuesta += "<br><br>" + FORMULARIO
        return HttpResponseNotFound(respuesta)

    respuesta = "Id: " + str(pagina.id) + "<br>"
    respuesta += "Nombre: " + pagina.name + "<br>"
    respuesta += "Pagina: " + pagina.page + "<br>"

    if request.user.is_authenticated():
        respuesta += "<br><br>" + FORMULARIO
    return HttpResponse(respuesta)
