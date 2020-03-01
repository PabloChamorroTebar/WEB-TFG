from PracticasUpm.classes import Practica, Alumno
import datetime
import hashlib


def create_asignaturas(json_praticas, json_asignaturas):
    practicas = {}
    for json_practica in json_praticas:
        print(json_practica)
        id = json_practica['idpractica']
        nombre = json_practica['nombre']
        creacion_grupo = json_practica['creacion_grupo']
        cierre_grupo = json_practica['cierre_grupo']
        entrega_practica = json_practica['entrega_practica']
        enunciado = json_practica['enunciado']
        personas_grupo = json_practica.get('personas_grupo')
        asignatura_idasignatura = json_practica['asignatura_idasignatura']
        practica = Practica(id, nombre, creacion_grupo, cierre_grupo, entrega_practica, personas_grupo, enunciado, asignatura_idasignatura)
        nombre_asginatura = name_by_id(json_asignaturas, asignatura_idasignatura)
        if practicas.get(nombre_asginatura) is None:
            # Quiere decir que no hay ninguna key con ese id
            practicas_asignatura = {}
        practicas_asignatura[nombre] = practica.__dict__
        practicas[nombre_asginatura] = practicas_asignatura
        # LLevarlo a otro metodo, que devuelva directamente las practicas , la key es el nombre y value practicas
    return practicas


def name_by_id (json_asignaturas, id):
    for json_asignatura in json_asignaturas:
        if json_asignatura['idasignatura'] == id:
            return json_asignatura['nombre']
    return None


def id_by_name (json_asignaturas, nombre):
    for json_asignatura in json_asignaturas:
        if json_asignatura['nombre'] == nombre:
            return json_asignatura['idasignatura']
    return None


# Metodo para insertar practica en la variable que contiene todas las practicas
def insert_practica_asignatura(practicas, practica, nombre_asignatura):
    if practicas.get(nombre_asignatura) is None:
        # Quiere decir que no hay ninguna key con ese id
        practicas[nombre_asignatura] = {}
    practicas[nombre_asignatura] = practicas.get(nombre_asignatura)
    practicas[nombre_asignatura][practica.nombre] = practica.__dict__
    # LLevarlo a otro metodo, que devuelva directamente las practicas , la key es el nombre y value practicas
    return practicas


# Metodo para insertar los grupos con los nombres de los alumnos en una variable
def create_grupos(json_grupos):
    grupos = {}
    for json_grupo in json_grupos:
        if grupos.get(json_grupo['grupo'].replace("'", "")) is None:
            grupos[json_grupo['grupo'].replace("'", "")] = [json_grupo['nombre']]
        else:
            grupos[json_grupo['grupo'].replace("'", "")].append(json_grupo['nombre'])
    return grupos


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def dict_noticias(noticias_list):
    noticias = {}
    noticias_result = {}
    for noticia in noticias_list:

        noticia_dict = {}
        noticia_dict['dia_semana'] = noticia.dia_semana
        noticia_dict['noticia'] = noticia.noticia
        noticia_dict['fecha'] = noticia.fecha.strftime("%Y-%m-%d %H:%M:%S")
        noticia_dict['mes'] = noticia.mes

        if not noticias.get(noticia.mes):
            noticias[noticia.mes] = [noticia_dict]
        else:
            noticias.get(noticia.mes).append(noticia_dict)

    # Ordenamos las fechas en funcion creciente
    months_curse = ["Septiembre", "Octubre", "Noviembre", "Diciembre", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto"]

    # Cogemos el mes actual
    month = datetime.datetime.now().month
    # Le restamos 9
    month = month - 9
    # Si es negativo sumamos 12 menos lo que sea
    month = month + 12
    # Y cogemos a partir de ahi
    i = 0
    while i <= month:
        months_curse.pop(0)
        i = i+1

    for month_curse in months_curse:
        if noticias.get(month_curse):
            noticias_result[month_curse] = noticias.get(month_curse)
    return noticias_result


# Metodo que crea un diccionario para luego poder iterar en la template y mostrar los alumnos en texto plano por grupo
def create_alumnos_grupo_text(json_alumnos_grupo_text):
    alumnos_grupo_text = {}

    # Iteramos sobre el json para ir alumno por alumno
    for json_alumno in json_alumnos_grupo_text:

        # Obtenemos las variables para crear el Alumno
        nombre_grupo = json_alumno['nombre_grupo']
        nombre = json_alumno['nombre']
        email = json_alumno['email']
        matricula = json_alumno['matricula']
        practica_idpractica = json_alumno['practica_idpractica']

        # Creamos el alumnos
        alumno = Alumno(nombre_grupo, nombre, email, matricula, practica_idpractica)

        # Comprobamos si existe el nombre grupo, sino lo creamos y si existe, lo insertamos
        if alumnos_grupo_text.get(nombre_grupo) is not None:
            alumnos_grupo_text.get(nombre_grupo).append(alumno.__dict__)

        else:
            alumnos_grupo_text[nombre_grupo] = [alumno.__dict__]

    return alumnos_grupo_text

