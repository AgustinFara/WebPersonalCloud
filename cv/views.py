from django.shortcuts import render
from django.db.models import Min, Max
from django.db.models.functions import Lower
import datetime
from .models import Work, Technology, Category


def tech(request):
    categories = Category.objects.all().prefetch_related('technologies')
    return render(request, 'cv/tech.html', {'categories': categories})

""""
def tech(request):
    techs = Technology.objects.all()
    return render(request, 'cv/tech.html', {'techs': techs})
"""


def about(request):
    works = Work.objects.all()

    # --- Agrego script para la edad ---
    fecha_nacimiento = datetime.date(1984, 3, 4)
    hoy = datetime.date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    # ------------------------------

# VALOR POR DEFECTO: Me aseguro la variable esté siempre con un valor.
    exp_mainframe = 20

# 2. Filtrar solo los trabajos de Mainframe
    works_mainframe = Work.objects.annotate(
        desc_lower=Lower('description')
    ).filter(desc_lower__contains='mainframe') # Buscamos siempre en minúscula

    # Traemos la fecha del primer trabajo y del último en una sola consulta
    fechas = works_mainframe.aggregate(
        primer_dia=Min('datestart'),
        ultimo_dia=Max('datefinish')
    )

    primer_dia = fechas['primer_dia']
    ultimo_dia = fechas['ultimo_dia']

    # 3. Calcular la diferencia de años en Python
    if primer_dia and ultimo_dia:
        # Convertimos a formato datetime.date si es que la BD devuelve datetime completo
        if isinstance(primer_dia, datetime.datetime):
            primer_dia = primer_dia.date()
        if isinstance(ultimo_dia, datetime.datetime):
            ultimo_dia = ultimo_dia.date()

    # Calculamos el total de meses reales entre las dos fechas
        total_meses = (ultimo_dia.year - primer_dia.year) * 12 + (ultimo_dia.month - primer_dia.month)

        anios_base = total_meses // 12
        meses_restantes = total_meses % 12

        #Si pasaron 9 meses o más, redondeamos para arriba
        if meses_restantes >= 9:
            exp_mainframe = anios_base + 1
        else:
            exp_mainframe = anios_base

    return render(request, "cv/about.html", {
        'works': works,
        'edad': edad,
        'exp_mainframe': exp_mainframe
    })


def cv(request):
    works = Work.objects.all()

    return render(request, "cv/cv.html", {'works':works})
