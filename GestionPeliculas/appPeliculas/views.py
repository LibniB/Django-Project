from django.shortcuts import render, redirect
from django.db import Error
from appPeliculas.models import Genero, Pelicula
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from bson import ObjectId

# Create your views here.


def inicio(request):
    return render(request, "inicio.html")

def vistaAgregarGenero(request):
    return render(request, "agregarGenero.html")

def agregarGenero(request):
    try:
        nombre = request.POST['txtNombre']
        genero = Genero(genNombre=nombre)
        genero.save()
        mensaje = "Genero Agregado Correctamente"
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje}
    # return JsonResponse(retorno)
    return render(request, "agregarGenero.html", retorno)


def listarPeliculas(request):
    peliculas = Pelicula.objects.all()

    retorno = {"peliculas": peliculas}
    return render(request, "listarPeliculas.html", retorno)


def vistaAgregarPelicula(request):
    generos = Genero.objects.all()

    retorno = {"generos": generos}
    return render(request, "agregarPelicula.html", retorno)


def agregarPelicula(request):
    try:
        codigo = request.POST['txtCodigo']
        titulo = request.POST['txtTitulo']
        protagonista = request.POST['txtProtagonista']
        duracion = int(request.POST['txtDuracion'])
        resumen = request.POST['txtResumen']
        foto = request.FILES['fileFoto']
        idGenero = ObjectId(request.POST['cbGenero'])
        genero = Genero.objects.get(pk=idGenero)
        # crear objeto pelicula
        pelicula = Pelicula(pelCodigo=codigo,
                            pelTitulo=titulo,
                            pelProtagonista=protagonista,
                            pelDuracion=duracion,
                            pelResumen=resumen,
                            pelFoto=foto,
                            pelGenero=genero)
        pelicula.save()
        mensaje = "Pelicula agregada correctamente"
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje, 'idPelicula': pelicula.pk}
    # return JsonResponse(retorno)
    return render(request, "agregarPelicula.html", retorno)


def consultarPeliculaPorId(request, id):
    pelicula = Pelicula.objects.get(pk=ObjectId(id))

    generos = Genero.objects.all()
    retorno = {"pelicula": pelicula, "generos": generos}
    return render(request, "actualizarPelicula.html", retorno)


def actualizarPelicula(request):
    try:
        idPelicula = ObjectId(request.POST['idPelicula'])
        peliculaActualizar = Pelicula.objects.get(pk=idPelicula)
       
        peliculaActualizar.pelCodigo = request.POST['txtCodigo']
        peliculaActualizar.pelTitulo = request.POST['txtTitulo']
        peliculaActualizar.pelProtagonista = request.POST['txtProtagonista']
        peliculaActualizar.pelDuracion = int(request.POST['txtDuracion'])
        peliculaActualizar.pelResumen = request.POST['txtResumen']
        idGenero = ObjectId(request.POST['cbGenero'])
        genero = Genero.objects.get(pk=idGenero)
        peliculaActualizar.pelGenero = genero
        foto = request.FILES.get('fileFoto')

        if (foto):
            if (peliculaActualizar.pelFoto != ""): 
                os.remove(os.path.join(settings.MEDIA_ROOT + "/" +
                                       str(peliculaActualizar.pelFoto)))
     
            peliculaActualizar.pelFoto = foto

        peliculaActualizar.save()
        mensaje = "Pelicula Actualizada"
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje}
    # return JsonResponse(retorno)
    return redirect("/listarPeliculas")


def eliminarPelicula(request, id):
    try:
        peliculaAEliminar = Pelicula.objects.get(pk=ObjectId(id))

        peliculaAEliminar.delete()
        mensaje = "Pelicula Eliminada Correctamente"
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje}
    # return JsonResponse(retorno)
    return redirect('/listarPeliculas')