from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from collections import namedtuple
import codecs
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from PracticasUpm.classes import *
from PracticasUpm.operations import *
from Tfg import settings
import PracticasUpm.operations
from . import classes
import requests, io
from datetime import date
from datetime import datetime
import array
import os
import csv



# Create your views here.


@login_required
def index(request):
    # Sacamos el profesor de la request
    profesor_request = request.session.get('profesor')

    # Transformamos el dict del profesor a la clase profesor para trabajar mas comodo
    profesor = namedtuple("Profesor", profesor_request.keys())(*profesor_request.values())

    # Insertamos en la request la asignatura
    insert_asignaturas_request(request, profesor)

    json_profesor_asgnaturas = request.session['asignaturas']

    # Insertamos en la request las practicas
    insert_practicas_request(request)

    practicas = request.session['practicas']
    # Creamos las tareas, las organizamos por mes , ponemos el dia de la semana y el dia mas la tarea
    noticias = []
    for key, value in practicas.items():
        for key, practica in value.items():
            noticia = Noticia(practica['creacion_grupo'], "Creación de los grupos de " + practica['nombre'])
            noticias.append(noticia)
            noticia = Noticia(practica['cierre_grupo'], "Cierre de los grupos de " + practica['nombre'])
            noticias.append(noticia)
            noticia = Noticia(practica['entrega_practica'], "Entrega de la practica " + practica['nombre'])
            noticias.append(noticia)

    noticias = dict_noticias(noticias)

    request.session['noticias'] = noticias

    if json_profesor_asgnaturas is not None:
        asignaturas = {}
        for json_asignatura in json_profesor_asgnaturas:
            id = json_asignatura['idasignatura']
            nombre = json_asignatura['nombre']
            guia_docente = json_asignatura['guia_docente']
            asignatura = Asginatura(id, nombre, guia_docente)
            asignaturas[nombre] = asignatura
    return render(request, 'PracticasUpm/index.html', {'asignaturas': asignaturas, 'noticias': noticias})


def login_view(request):
    return render(request, 'PracticasUpm/login.html', None)


# function check if user and password exits
def check_login(request):
    if request.POST:
        # Obtain user and password
        json_data = json.loads(request.body)
        user = json_data['user']
        password = json_data['password']

        # Convert password t sha256
        password = encrypt_string(password)

        # Call api and check if user exist and check password
        # sending post request and saving response as response object
        url = settings.STATIC_API + 'login_profesores/'
        payload = {"email": "" + user + ""}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        json_profesor = json.loads(response._content)

        try:
            # Check if profesor exist
            id = json_profesor[0]['idprofesor']
            nombre = json_profesor[0]['nombre']
            email = json_profesor[0]['email']
            password_profesor = json_profesor[0]['password']
            profesor = Profesor(id, nombre, email, password_profesor)

            # save profesor in request
            request.session['profesor'] = profesor.__dict__

            # check is passwords are equals
            if profesor.password != password:
                response = JsonResponse({'error': 'Wrong user or password'})
                response.status_code = 400
                return response

            # Create user profesor to authenticate
            profesor = User.objects.create_user(profesor.name, profesor.email, profesor.password)

            # we authenticate like profesor
            user = authenticate(request, username=profesor.name, password=profesor.password)
            login(request, user)

            response = json.dumps({'url': settings.URL_BASE + 'PracticasUpm/'})
            return JsonResponse(response, safe=False)
        except ValueError:
            response = JsonResponse({'error': 'Wrong user or password'})
            response.status_code = 400
            return response
        except IntegrityError:
            # we authenticate like profesor
            user = authenticate(request, username=profesor.name, password=profesor.password)
            login(request, user)
            response = json.dumps({'url': settings.URL_BASE + 'PracticasUpm/'})
            return JsonResponse(response, safe=False)


@login_required
def do_logout(request):
    if request.method == 'GET':
        logout(request)
        response = json.dumps({'url': settings.URL_BASE + 'PracticasUpm/'})
        return JsonResponse(response, safe=False)


@login_required
def school_calendar(request):
    if request.method == 'GET':
        html = render(request, 'PracticasUpm/school_calendar.html')
        html = "\"" + html.content.decode("utf-8") + "\""
        response = json.dumps({'html': html})
        return JsonResponse(response, safe=False)


@login_required
def go_asignatura(request, asignatura):
    if request.method == 'GET':
        response = json.dumps({'url': settings.URL_BASE + 'PracticasUpm/asignaturas/' + asignatura})
        return JsonResponse(response, safe=False)


@login_required
def asignatura(request, asignatura):
    if request.session.get('practicas') is None:

        insert_practicas_request(request)

    else:
        practicas = request.session.get('practicas')
    # Adquirimoslas practicas en dicha asignatura
    if practicas.get(asignatura) is not None:
        practicas_asignatura = practicas[asignatura]
    else:
        practicas_asignatura = {}

    # Cogemos todas las asignaturas para el navbar
    json_profesor_asgnaturas = request.session.get('asignaturas')
    if json_profesor_asgnaturas is not None:
        asignaturas = {}
        for json_asignatura in json_profesor_asgnaturas:
            id = json_asignatura['idasignatura']
            nombre = json_asignatura['nombre']
            guia_docente = json_asignatura['guia_docente']
            asignatura_actual = Asginatura(id, nombre, guia_docente)
            asignaturas[nombre] = asignatura_actual
    return render(request, 'PracticasUpm/asignatura.html', {'practicas_asignatura': practicas_asignatura,
                                                            'asignatura': asignatura, 'asignaturas': asignaturas})


@login_required
def create_practica(request, asignatura):
    return render(request, 'PracticasUpm/create_practica.html', {'asignatura': asignatura})


@login_required
def save_practica(request, asignatura):
    if request.method == 'POST' and request.FILES['document'] is not None and request.FILES['document'].content_type == 'application/pdf':
        print(request.POST)
        pdfFileObj = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(pdfFileObj.name, pdfFileObj)
        file = fs.path(filename)

        # Create struct to send in json
        payload = {}
        payload['nombre'] = request.POST['nombre']
        payload['creacion_grupo'] = request.POST['creacion_grupos']
        payload['cierre_grupo'] = request.POST['cierre_grupos']
        payload['entrega_practica'] = request.POST['entrega_practica']
        payload['personas_grupo'] = request.POST['personas_grupo']
        json_asignaturas = request.session.get('asignaturas')
        payload['asignatura_idasignatura'] = id_by_name(json_asignaturas, asignatura)

        url = settings.STATIC_API + 'asignaturas/' + str(id_by_name(json_asignaturas, asignatura)) + '/practicas'

        files = {
            'json': (None, json.dumps(payload), 'application/json'),
            'file': (file, open(file, 'rb'), 'application/octet-stream')
        }

        # Borramos el fichero
        os.unlink(file)

        headers = {'content-type': 'application/json'}
        response = requests.post(url, files=files, data=payload)
        if response.status_code == 200:
            json_practicas = request.session['practicas']
            id = id_by_name(json_asignaturas, asignatura)
            request.session['practicas'] = insert_practica_asignatura(json_practicas, Practica(json.loads(response.content)[0]['idpractica'],
                                                                request.POST['nombre'], request.POST['creacion_grupos'],
                                                                request.POST['cierre_grupos'],
                                                                request.POST['entrega_practica'],
                                                                request.POST['personas_grupo'], json.loads(response.content)[0]['enunciado'],
                                                                id), asignatura)
            practicas_asignatura = json_practicas[asignatura]
            # Cogemos todas las asignaturas para el navbar
            json_profesor_asgnaturas = request.session.get('asignaturas')
            if json_profesor_asgnaturas is not None:
                asignaturas = {}
                for json_asignatura in json_profesor_asgnaturas:
                    id = json_asignatura['idasignatura']
                    nombre = json_asignatura['nombre']
                    guia_docente = json_asignatura['guia_docente']
                    asignatura_actual = Asginatura(id, nombre, guia_docente)
                    asignaturas[nombre] = asignatura_actual
                print(asignaturas)
            return render(request, 'PracticasUpm/asignatura.html',
                          {'practicas_asignatura': practicas_asignatura, 'asignatura': asignatura,
                           'asignaturas': asignaturas})
        # Else: ha habido algun error HHHHHHHAAAACERRRR
    return index(request)


@login_required
def go_create(request, asignatura):
    if request.method == 'GET':
        response = json.dumps({'url': settings.URL_BASE + 'PracticasUpm/asignaturas/' + asignatura + '/practicas/create'})
        return JsonResponse(response, safe=False)


@login_required
def practica(request, asignatura, practica):

    # Obtain from request asignaturas and practicas
    json_profesor_asgnaturas = request.session['asignaturas']
    json_profesor_practicas = request.session['practicas']

    if json_profesor_asgnaturas is not None and json_profesor_practicas is not None:
        asignaturas = {}
        for json_asignatura in json_profesor_asgnaturas:
            id = json_asignatura['idasignatura']
            nombre = json_asignatura['nombre']
            guia_docente = json_asignatura['guia_docente']
            _asignatura = Asginatura(id, nombre, guia_docente)
            asignaturas[nombre] = _asignatura
        practica = json_profesor_practicas[asignatura][practica]

        # Cehck if currernt date is less or more than cierre grupo
        if practica['cierre_grupo'].find('T') != -1:
            practica_cierre_grupo = practica['cierre_grupo'][:practica['cierre_grupo'].find('T')]
        else:
            practica_cierre_grupo = practica['cierre_grupo']
        if datetime.strptime(practica_cierre_grupo, '%Y-%m-%d') > datetime.today():
            url = settings.STATIC_API + 'asignaturas/' + str(practica['asignatura_idasignatura']) + '/practicas/' + str(practica['id']) +'/grupos_alumno'
            headers = {'content-type': 'application/json'}
            response = requests.get(url, headers=headers)
            json_grupos = json.loads(response.content)
            grupos = create_grupos(json_grupos)
            return render(request, 'PracticasUpm/practica.html', {'asignaturas': asignaturas, 'practica': practica,
                            'asignatura': asignatura, 'grupos': grupos, 'practica_nombre': practica['nombre'], 'show_grupos': True})
        else:
            return render(request, 'PracticasUpm/practica.html', {'asignaturas': asignaturas, 'practica': practica,
                            'asignatura': asignatura, 'practica_nombre': practica['nombre']})


@login_required
def go_practica (request, asignatura, practica):
    if request.method == 'GET':
        response = json.dumps({'url': settings.URL_BASE + 'PracticasUpm/asignaturas/' + asignatura + '/practicas/' + practica})
        return JsonResponse(response, safe=False)


@login_required
def show_enunnciado (request, asignatura, practica):
    if request.method == 'GET':
        json_practicas = request.session['practicas']

        # Sacamos el buffer
        enunciado = json_practicas[asignatura][practica]['enunciado']['data']

        # Lo convertimos para mostrar el pdf
        enunciado = array.array('B', enunciado).tostring().decode('ISO8859-1').encode('ISO8859-1')

        response = HttpResponse(enunciado, content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=enunciado.pdf'
        return response


@login_required
def show_guia_docente (request, asignatura):
    if request.method == 'GET':
        json_asignaturas = request.session['asignaturas']

        # Cogemos la positicion
        contador = 0
        for asignatura_json in json_asignaturas:
            if asignatura_json['nombre'] == asignatura:
                break
            else:
                contador = contador +1

        # Sacamos el buffer
        enunciado = json_asignaturas[contador]['guia_docente']['data']

        # Lo convertimos para mostrar el pdf
        enunciado = array.array('B', enunciado).tostring().decode('ISO8859-1').encode('ISO8859-1')

        response = HttpResponse(enunciado, content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=enunciado.pdf'

        return response


@login_required
def show_grupos (request, asignatura, practica):
    if request.method == 'GET':
        json_profesor_practicas = request.session['practicas']
        url = settings.STATIC_API + 'asignaturas/' + str(json_profesor_practicas[asignatura][practica]['asignatura_idasignatura']) + '/practicas/' \
              + str(json_profesor_practicas[asignatura][practica]['id']) + '/pdf_grupos'
        headers = {'content-type': 'application/json'}
        response = requests.get(url, headers=headers)
        json_pdf_grupos = json.loads(response.content)
        pdf_grupos = json_pdf_grupos[0]['pdf_grupos']['data']

        # Lo convertimos para mostrar el pdf
        pdf_grupos = array.array('B', pdf_grupos).tostring().decode('ISO8859-1').encode('ISO8859-1')
        response = HttpResponse(pdf_grupos, content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=enunciado.pdf'
        return response


@login_required
def go_to_show_groups_text_plain (request, asignatura, practica):
    response = json.dumps({'url': settings.URL_BASE + 'PracticasUpm/asignaturas/' + asignatura + '/practicas/'
                                                    + practica + '/grupos_texto_plano'})
    return JsonResponse(response, safe=False)


@login_required
def show_groups_text_plain (request, asignatura, practica):
    if request.method == 'GET':

        # Obtenemos la practica
        json_profesor_practicas = request.session['practicas']
        practica = json_profesor_practicas[asignatura][practica]

        # Hacemos una llamada para conseguir los grupos de esa practica
        url = settings.STATIC_API + 'asignaturas/' + str(practica['asignatura_idasignatura']) +\
              '/practicas/' + str(practica['id']) + '/grupos_texto_plano'
        headers = {'content-type': 'application/json'}
        response = requests.get(url, headers=headers)
        json_grupos = json.loads(response.content)

        # Creamos a los grupos
        alumnos_grupo_text = create_alumnos_grupo_text(json_grupos)

        # Mostramos la pagina

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="gruposAlumnos.csv"'

        writer = csv.writer(response)
        writer.writerow(['Nombre Grupo', 'Nombre Alumno', 'Email', 'Matricula'])

        for key, value in alumnos_grupo_text.items():
            for alumno in value:
                writer.writerow([alumno['nombre_grupo'], alumno['nombre'], alumno['email'], alumno['matricula']])

        return response

# return render(request, 'PracticasUpm/block_grupos_plain_text.html', {'alumnos_grupo_text': alumnos_grupo_text})


def insert_asignaturas_request(request, profesor):
    # Call to asignturas_profesores
    url = settings.STATIC_API + 'asignaturas_profesor/' + str(profesor.id)
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)

    json_profesor_asgnaturas = json.loads(response.content)

    request.session['asignaturas'] = json_profesor_asgnaturas


def insert_practicas_request(request):
    # Sacamos el profesor de la request
    profesor_request = request.session.get('profesor')

    # Transformamos el dict del profesor a la clase profesor para trabajar mas comodo
    profesor = namedtuple("Profesor", profesor_request.keys())(*profesor_request.values())

    # Sacamos las asignaturas de la request
    json_asignaturas = request.session.get('asignaturas')

    # Obtenemos de la api las practicas de este profesor
    url = settings.STATIC_API + 'profesores/' + str(profesor.id) + '/practicas_profesor'
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)

    json_practicas = json.loads(response.content)
    practicas = create_asignaturas(json_practicas, json_asignaturas)

    # Metemos en la session las practicas
    request.session['practicas'] = practicas
