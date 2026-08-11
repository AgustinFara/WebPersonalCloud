# ==============================================================================
# IMPORTS
# ==============================================================================

import importlib
import os
from unittest import mock

from django.test import SimpleTestCase

# ==============================================================================
# Clase de prueba para validar la carga de settings y variables de entorno
# ==============================================================================

class SettingsTestCase(SimpleTestCase):

    # ==========================================================================
    # Configuración de entorno de prueba
    # ==========================================================================

    def setUp(self):
        # Entorno completo válido con TODAS las variables necesarias
        self.env_valido = {
            'GOOGLE_APPLICATION_CREDENTIALS': '/path/fake.json',
            'DEBUG': 'True',
            'ALLOWED_HOSTS': 'localhost 127.0.0.1',
            'SECRET_KEY': 'clave-de-prueba-super-secreta',
            'DB_SCHEMA': 'public',
            'DB_URL': 'postgres://user:pass@localhost:5432/db',
            'SUPABASE_ACCESS_KEY': 'fake_access_key',
            'SUPABASE_SECRET': 'fake_secret',
            'SUPABASE_PROJECT_ID': 'fake_project_id',
        }

    # ==========================================================================
    # Tests 1 - Validación de carga de settings con entorno completo
    # ==========================================================================

    def test_settings_cargan_correctamente_con_env(self):
        with mock.patch("dotenv.load_dotenv"), \
                mock.patch("os.path.exists", return_value=True), \
                mock.patch.dict(os.environ, self.env_valido, clear=True):

            import webpersonal.settings as app_settings
            importlib.reload(app_settings)

            self.assertEqual(app_settings.SECRET_KEY,
                             'clave-de-prueba-super-secreta')
            self.assertEqual(app_settings.ALLOWED_HOSTS,
                             ['localhost', '127.0.0.1'])
            self.assertTrue(app_settings.DEBUG)

    # ==========================================================================
    # Tests 2 - Validación de carga de settings sin secret key
    # ==========================================================================

    def test_settings_lanza_error_si_falta_secret_key(self):
        env_sin_secret = self.env_valido.copy()
        del env_sin_secret['SECRET_KEY']  # Omitimos ÚNICAMENTE la SECRET_KEY

        with mock.patch("dotenv.load_dotenv"), \
                mock.patch("os.path.exists", return_value=True), \
                mock.patch.dict(os.environ, env_sin_secret, clear=True):

            import webpersonal.settings as app_settings

            with self.assertRaises(ValueError) as context:
                importlib.reload(app_settings)

            msg_esperado = (
                "CRÍTICO: No se puede iniciar la web sin una "
                "SECRET_KEY configurada."
            )

            self.assertIn(msg_esperado, str(context.exception))

    # ==========================================================================
    # Tests 3 - Validación de carga de settings sin Supabase Secret
    # ==========================================================================

    def test_settings_lanza_error_si_falta_supabase_secret(self):
        env_sin_supabase = self.env_valido.copy()
        # Omitimos el secret de Supabase
        del env_sin_supabase['SUPABASE_SECRET']

        with mock.patch("dotenv.load_dotenv"), \
                mock.patch("os.path.exists", return_value=True), \
                mock.patch.dict(os.environ, env_sin_supabase, clear=True):

            import webpersonal.settings as app_settings

            with self.assertRaises(ValueError) as context:
                importlib.reload(app_settings)

            msg_esperado = (
                "CRÍTICO: No se puede iniciar la web sin la "
                "variable Supabase secret."
            )

            self.assertIn(msg_esperado, str(context.exception))
