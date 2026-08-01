# ==============================================================================
# IMPORTS
# ==============================================================================
import os
import sys
import google.auth
from google.auth.exceptions import DefaultCredentialsError

# ==============================================================================
# Funcion que valida Google Application Credentials y la devuelve en settings.py
# ==============================================================================
def validar_google_aplication_credentials():
    # 1. Si existe la variable con la ruta al archivo JSON
    json_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if json_path and os.path.exists(json_path):
        print("✅ GCP Config: Se encontró archivo JSON de credenciales.")
        return True

    # 2. O si tienes el contenido del JSON en una variable de entorno
    if os.getenv('GCP_SA_KEY') or os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'):
        print("✅ GCP Config: Se encontró contenido de credenciales en variable de entorno.")
        return True

    # 3. O si estamos en Cloud Run (Google define la variable K_SERVICE en Cloud Run)
    if os.getenv('K_SERVICE'):
        print("✅ GCP Config: Ejecutando en Cloud Run (Autenticación nativa habilitada).")
        return True

    # Si no cumple ninguna de las anteriores, falta la configuración
    raise ValueError(
        "⛔ CRÍTICO: Falta la configuración de credenciales de Google "
        "(No hay JSON, no hay GCP_SA_KEY ni se detectó entorno Cloud Run)."
    )



# ==============================================================================
# Funcion que valida variable de debug y la devuelve en settings.py
# ==============================================================================

def validar_debug():
    #Verifico si la variable de entorno DEBUG está definida y la asigno a la variable DEBUG
    DEBUG_ENV = os.environ.get('DEBUG')

    if DEBUG_ENV == 'True':
        DEBUG = True
        print("✅ Debug activado desde las variables de entorno.")
    elif DEBUG_ENV == 'False':
        DEBUG = False
        print("✅ Debug desactivado desde las variables de entorno.")
    else:
        DEBUG = False
        print("⚠️ ADVERTENCIA: No se encontró variable de debug se mantiene desactivado.")

    return DEBUG



# ==============================================================================
# Funcion que valida variable de allowed hosts y la devuelve en settings.py
# ==============================================================================

def validar_allowed_hosts():
    #Asigno el valor de ALLOWED_HOSTS desde la variable de entorno 'ALLOWED_HOSTS' para producción
    ALLOWED_HOSTS_RAW = os.environ.get('ALLOWED_HOSTS')
    if ALLOWED_HOSTS_RAW:
        ALLOWED_HOSTS = ALLOWED_HOSTS_RAW.split(',')
        print(f"✅ ALLOWED_HOSTS cargado: {ALLOWED_HOSTS}")
        return ALLOWED_HOSTS
    else:
        ALLOWED_HOSTS = []  # Lista vacía = Bloqueo total
        raise ValueError("⛔ CRÍTICO: No se puede iniciar la aplicación sin una la variable ALLOWED_HOSTS configurada.")



# ==============================================================================
# Funcion que valida variable secret key y la devuelve en settings.py
# ==============================================================================

def validar_secret_key():
    #Asigno el valor de SECRET_KEY desde la variable de entorno 'SECRET_KEY' para producción
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if SECRET_KEY:
        print("✅ SECRET_KEY cargada correctamente desde las variables de entorno.")
        return SECRET_KEY
    else:
        raise ValueError("⛔ CRÍTICO: No se puede iniciar la web sin una SECRET_KEY configurada.")



# ==============================================================================
# Funcion que valida el schema ingresado y la devuelve en settings.py
# ==============================================================================

def validar_schema():
    #Asigno a la variable DB_SCHEMA el valor de la variable de entorno 'DB_SCHEMA'
    # dev es el schema de desarrollo, mientras que public es el schema para la version productiva
    DB_SCHEMA = os.environ.get('DB_SCHEMA')

    if DB_SCHEMA:
        print(f"✅ DB_SCHEMA cargado correctamente desde las variables de entorno.({DB_SCHEMA})")
        return DB_SCHEMA
    else:
        raise ValueError("⛔ CRÍTICO: No se puede iniciar la web sin un DB_SCHEMA configurado.")



# ==============================================================================
# Funcion que valida el la variable db_url y la devuelve en settings.py
# ==============================================================================

def validar_db_url():
    #Asigno a la variable DB_URL el valor de la variable de entorno 'DB_URL' si existe
    DB_URL = os.environ.get('DB_URL')

    if DB_URL:
        print(f"✅ DB_URL cargado correctamente desde las variables de entorno.")
        return DB_URL
    else:
        raise ValueError("⛔ CRÍTICO: No se puede iniciar la web sin un DB_URL configurado.")



# ==============================================================================
# Funcion que valida el la variable supabase_secret y la devuelve en settings.py
# ==============================================================================

def validar_supabase_secret():
    #Asigno a la variable SUPABASE_ACCESS_KEY y SUPABASE_SECRET el valor de las variables de entorno correspondientes
    SUPABASE_SECRET = os.environ.get('SUPABASE_SECRET')

    if SUPABASE_SECRET:
        print("✅ Supabase secret cargado correctamente desde las variables de entorno.")
        return SUPABASE_SECRET
    else:
        raise ValueError("⛔ CRÍTICO: No se puede iniciar la web sin las variable Supabase secret.")



# ==============================================================================
# Funcion que valida el la variable supabase_access_key y la devuelve en settings.py
# ==============================================================================
def validar_supabase_access_key():
    #Asigno a la variable SUPABASE_ACCESS_KEY y SUPABASE_SECRET el valor de las variables de entorno correspondientes
    SUPABASE_ACCESS_KEY = os.environ.get('SUPABASE_ACCESS_KEY')

    if SUPABASE_ACCESS_KEY:
        print("✅ Supabase access key cargada correctamente desde las variables de entorno.")
        return SUPABASE_ACCESS_KEY
    else:
        raise ValueError("⛔ CRÍTICO: No se puede iniciar la web sin Supabase access key configurada.")



# ==============================================================================
# Funcion que valida el la variable supabase_project_id y la devuelve en settings.py
# ==============================================================================

def validar_supabase_project_id():
    #Asigno a la variable SUPABASE_PROJECT_ID el valor de la variable de entorno correspondiente
    SUPABASE_PROJECT_ID = os.environ.get('SUPABASE_PROJECT_ID')

    if SUPABASE_PROJECT_ID:
        print("✅ Supabase project id cargado correctamente desde las variables de entorno.")
        return SUPABASE_PROJECT_ID
    else:
        raise ValueError("⛔ CRÍTICO: No se puede iniciar la web sin Supabase project id configurado.")


