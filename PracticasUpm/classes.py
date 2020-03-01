# Define all classes in this file
import datetime


class Profesor:

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


class Asginatura:

    def __init__(self, id, nombre, guia_docente):
        self.id = id
        self.nombre = nombre
        self.guia_docente = guia_docente


class Practica:

    def __init__(self, id, nombre, creacion_grupo, cierre_grupo, entrega_practica, personas_grupo, enunciado, asignatura_idasignatura ):
        self.id = id
        self.nombre = nombre
        self.creacion_grupo = creacion_grupo
        self.cierre_grupo = cierre_grupo
        self.entrega_practica = entrega_practica
        self.personas_grupo = personas_grupo
        self.enunciado = enunciado
        self.asignatura_idasignatura = asignatura_idasignatura


class Grupo:

    def __init__(self, id, nombre, practica_idpractica):
        self.id = id
        self.nombre = nombre
        self.practica_idpractica = practica_idpractica


class Noticia:

    def __init__(self, fecha, noticia):
        weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        fecha = fecha[0:fecha.find('T')]
        fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
        fecha += datetime.timedelta(days=1)
        self.dia_semana = weekDays[fecha.weekday()] + " " + str(fecha.day)
        self.noticia = noticia
        self.fecha = fecha
        self.mes = months[fecha.month-1]


# Esta clase sirve para mostrar el alumno en el texto plano con sus atributos
class Alumno:

    def __init__(self, nombre_grupo, nombre, email, matricula, practica_idpractica):
        self.nombre_grupo = nombre_grupo.replace("'", "")
        self.nombre = nombre
        self.email = email
        self.matricula = matricula
        self.practica_idpractica = practica_idpractica
