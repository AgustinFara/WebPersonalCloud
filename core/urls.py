from django.urls import path

from . import views

# patts de la app polls
app_name = 'core'
urlpatterns = [
    # ex: /polls/
    path('', views.home, name='home'),  # Home de la página
    #   path('about', views.about, name='about'), #Página acerca de:
    #   path('portfolio', views.portfolio, name='portfolio'), #Página de portfolio
    path('contact', views.contact, name='contact'),  # Página de contacto
    path('chart', views.chart, name='chart'),  # Página de contacto
    path('chart/<str:fecha>/', views.chart,
         name='chart_con_fecha'),  # Caso con fecha
    path('noticias/<str:nombre>/<str:fecha>/',
         views.noticias_por_protagonista, name='ver_noticias'),
    # ex: /polls/5/
    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]
