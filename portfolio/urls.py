from django.urls import path
from . import views


#patts de la app polls
app_name = 'portfolio'
urlpatterns = [
    path('portfolio/', views.portfolio, name='portfolio'), #Página de portfolio
    path('cursos/', views.courses, name='cursos'), #Página de cursos

]