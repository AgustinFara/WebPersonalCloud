from django.shortcuts import render
from .models import Project, Course
# Create your views here.

def portfolio(request):
    projects = Project.objects.all()

    return render(request, "portfolio/portfolio.html", {'projects':projects})

def courses(request):
    courses = Course.objects.all()
    return render(request, "portfolio/cursos.html", {'courses': courses})