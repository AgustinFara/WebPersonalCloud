# ==============================================================================
# IMPORTS
# ==============================================================================

from django.db import connection
from django.db.models.signals import pre_migrate
from django.test.runner import DiscoverRunner

# ==============================================================================
# Creo un schema test aislado para las pruebas pytest
# ==============================================================================

def create_test_schema(sender, **kwargs):

    with connection.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS test;")


# ==============================================================================
# Creo el schema previo a correr las migraciones de test, y fuerzo el
# search_path a 'test' para que las migraciones se ejecuten en ese esquema.
# ==============================================================================

class PostgresSchemaTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # Me suscribo al evento pre_migrate para crear el esquema 'test'
        # antes de que se ejecuten las migraciones de prueba
        # es como el '+=' en C#
        pre_migrate.connect(create_test_schema)

        # 2. Forzamos el search_path a 'test'
        connection.settings_dict['OPTIONS']['options'] = '-c search_path=test'

        # 3. Django crea la BD de test y corre las migraciones
        # (ahora el esquema 'test' ya va a existir)
        return super().setup_databases(**kwargs)
