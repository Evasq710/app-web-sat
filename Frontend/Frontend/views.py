from django.http import HttpResponse
# (1) from django.template import Template, Context
# (2) from django.template import loader
# (3) :
from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def load_file(request):
    return render(request, "cargarArchivo.html")

def peticion_datos(request):
    return render(request, "consultarDatos.html")


# Funcion vista
def saludo(request):
    nombre = "Elias"
    apellido = "Vasquez"
    temas = ["Tema 1", "Tema 2", "Tema 3", "Tema 4"]

    # (1) === CARGANDO LA PLANTILLA MANUALMENTE (con Template y Context) ===
    # doc_html = open('G:/Mi unidad/USAC/2021/2 Semestre/IPC 2/LAB IPC2/Proyecto 3/IPC2_Proyecto3_201900131/Frontend/Frontend/templates/ejemplo.html')
    # temp = Template(doc_html.read())
    # doc_html.close()
    # # Definiendo variables en el contexto (puede ir vacío)
    # ctxt = Context({
    #     'nombre': nombre, 'apellido': apellido, 'temas': temas
    # })
    # # Renderizando la plantilla, mandándole el contexto
    # doc_renderizado = temp.render(ctxt)

    # return HttpResponse(doc_renderizado)


    # (2) === CARGANDO LA PLANTILLA CON UN LOADER, HABIENDO ESPECIFICADO LA RUTA DE LAS PLANTILLAS EN settings.py  ===
    # temp = loader.get_template('ejemplo.html')
    # doc_renderizado = temp.render({
    #     'nombre': nombre, 'apellido': apellido, 'temas': temas
    # })

    # return HttpResponse(doc_renderizado)


    # (3) === CARGANDO LA PLANTILLA CON RENDER DE SHORTCUTS, HABIENDO ESPECIFICADO LA RUTA DE LAS PLANTILLAS EN settings.py  ===
    # El contexto puede ir vacío
    return render(request, 'ejemplo.html', {'nombre': nombre, 'apellido': apellido, 'temas': temas})


def calcularEdad(request, edad, agno):
    periodo = agno - 2021
    edad_futura = edad + periodo
    respuesta = "<h2>En el año %s tendrás %s años.</h2>" %(agno, edad_futura)
    return HttpResponse(respuesta)