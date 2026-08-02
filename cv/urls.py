from django.urls import path

from . import views

# paths de la app CV
app_name = 'cv'
urlpatterns = [
    path('about', views.about, name='about'),  # Página sobre mi
    path('cv', views.cv, name='cv'),  # Experiencia Laboral
    path('tech', views.tech, name='tech'),  # Tecnologías
]
