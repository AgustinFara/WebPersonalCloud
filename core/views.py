import json
from datetime import date, timedelta

from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from google.cloud import bigquery

# Create your views here.

def home(request):
    return render(request, "core/home.html")


def contact(request):
    return render(request, "core/contact.html")


def chart(request, fecha=None):
    data = obtener_datos_bq(fecha)

    children = data.get('children')
    hay_datos = bool(children)

    data_json = json.dumps(data)

    return render(request, "core/chart.html", {
        'data_jerarquica': data_json,
        'mostrar_chart': hay_datos,
        'fecha': data['fecha'],
        'fecha_ant': data['fecha_ant'],
        'fecha_sig': data['fecha_sig'],
        'hoy': data['hoy'],
    })


def obtener_datos_bq(fecha=None):

    # 1. Definir fecha_actual
    if fecha:
        fecha_actual = date.fromisoformat(fecha)
    else:
        fecha_actual = timezone.localdate()

    # 2. Calcular fechas relativas
    fecha_str = fecha_actual.strftime('%Y-%m-%d')
    fecha_anterior = (fecha_actual - timedelta(days=1)).strftime('%Y-%m-%d')
    fecha_siguiente = (fecha_actual + timedelta(days=1)).strftime('%Y-%m-%d')
    hoy_str = timezone.localdate().strftime('%Y-%m-%d')

    data = None
    client = bigquery.Client()
    # Tu consulta ajustada para que los campos coincidan con lo que D3 espera: 'name' y 'value'
    query = """
        SELECT 
            n.Nombre_protagonista AS name,
            COUNT(n.noticia_id) AS value
        FROM `scrapnoticias-499802.news_analytics.noticias_procesadas` as n
        JOIN `scrapnoticias-499802.news_analytics.raw_noticias` AS p
        ON n.noticia_id = p.noticia_id 
        WHERE es_publicidad = False AND
        n.Nombre_protagonista <> '-'
        AND DATE(p.fecha_captura) = @fecha  -- Filtramos por el día exacto
        GROUP BY name
        HAVING value > 1
        ORDER BY value desc
        LIMIT 20
    """
    # 2. Configurar el parámetro correctamente
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("fecha", "STRING", fecha_str)
        ]
    )

    try:
        # LE paso el job config al query
        query_job = client.query(query, job_config=job_config)
        rows = list(query_job)
        if rows:
            # Construimos la lista con el campo 'link' extra
            children = []
            for row in rows:
                child = dict(row)
                # Asumiendo que tienes una ruta llamada 'noticias_por_protagonista'
                # Y que esta espera un argumento llamado 'nombre' y 'fecha'
                child['link'] = reverse('core:ver_noticias', kwargs={
                    'nombre': slugify(child['name']),
                    'fecha': fecha_str
                })
                children.append(child)

            data = {
                "name": "root",
                "children": children,
                'fecha': fecha_str,
                'fecha_ant': fecha_anterior,
                'fecha_sig': fecha_siguiente,
                'hoy': hoy_str,
            }
        else:
            data = {
                "name": None,
                "children": None,
                'fecha': fecha_str,
                'fecha_ant': fecha_anterior,
                'fecha_sig': fecha_siguiente,
                'hoy': hoy_str,
            }

    except Exception as e:
        print(f"Error en consulta BigQuery: {e}")

    return data


def noticias_por_protagonista(request, nombre, fecha):
    # 1. Convertir 'lionel-messi' -> 'Lionel Messi'
    # Esto es una aproximación; lo ideal es que si tu base tiene nombres con mayúsculas,
    # uses el nombre formateado correctamente.
    nombre_limpio = nombre.replace("-", " ").title()

    print(f"DEBUG: Buscando noticias para: '{nombre_limpio}'")

    client = bigquery.Client()

    # 2. Usar consultas parametrizadas (MUY RECOMENDADO por seguridad)
    query = """
        SELECT n.titulo, DATE(n.fecha_captura) as fecha, n.portal, COUNT(*) as frecuencia
        FROM `scrapnoticias-499802.news_analytics.raw_noticias` AS n 
        JOIN `scrapnoticias-499802.news_analytics.noticias_procesadas` AS p 
        ON n.noticia_id = p.noticia_id
        WHERE LOWER(p.Nombre_protagonista) = LOWER(@nombre)
        AND DATE(n.fecha_captura) = DATE(@fecha)
        GROUP BY titulo, portal, fecha
        ORDER BY frecuencia
    """

    # Crear el job configurando los parámetros
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("nombre", "STRING", nombre_limpio),
            bigquery.ScalarQueryParameter(
                "fecha", "DATE", fecha)  # Cambié a tipo DATE
        ]
    )

    query_job = client.query(query, job_config=job_config)
    # Convertir resultados a lista de diccionarios
    noticias = [dict(row) for row in query_job]

# CONVERSIÓN CRÍTICA: convertir fechas a string para que JS no rompa
    for n in noticias:
        if 'fecha' in n and hasattr(n['fecha'], 'strftime'):
            n['fecha'] = n['fecha'].strftime('%Y-%m-%d')

    print(f"DEBUG: Se encontraron {len(noticias)} noticias.")

    import json
    noticias_json = json.dumps(noticias)

    return render(request, "core/noticias.html", {
        'noticias': noticias,
        'noticias_json': noticias_json,
        'protagonista': nombre_limpio,
        'fecha': fecha
    })
