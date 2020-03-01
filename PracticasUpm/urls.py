from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('check_login', views.check_login, name='check_login'),
    path('logout', views.do_logout, name="logout"),
    path('school_calendar', views.school_calendar, name="school_calendar"),
    path('go_asignatura/<str:asignatura>', views.go_asignatura, name="go_asignatura"),
    path('asignaturas/<str:asignatura>', views.asignatura, name='asignatura'),
    path('asignaturas/<str:asignatura>/guia_docente', views.show_guia_docente, name='guia_docente'),
    path('asignaturas/<str:asignatura>/practicas/create', views.create_practica, name='create_practica'),
    path('asignaturas/<str:asignatura>/practicas/save', views.save_practica, name='save_practica'),
    path('asignaturas/<str:asignatura>/practicas/go_create', views.go_create, name='go_create'),
    path('asignaturas/<str:asignatura>/practicas/<str:practica>', views.practica, name='practica'),
    path('asignaturas/<str:asignatura>/go_practica/<str:practica>', views.go_practica, name='go_practica'),
    path('asignaturas/<str:asignatura>/practicas/<str:practica>/enunciado',
         views.show_enunnciado, name='show_enunciado'),
    path('asignaturas/<str:asignatura>/practicas/<str:practica>/pdf_grupos',
         views.show_grupos, name='pdf_grupos'),
    path('asignaturas/<str:asignatura>/practicas/<str:practica>/grupos_texto_plano',
         views.show_groups_text_plain, name='grupos_texto_plano'),
path('asignaturas/<str:asignatura>/practicas/<str:practica>/go_to_grupos_texto_plano',
         views.go_to_show_groups_text_plain, name='go_to_grupos_texto_plano'),
]
