import unittest

# Ruta de importación corregida
from util.utilidades import es_email_valido


class TestUtilidades(unittest.TestCase):
    def test_email_valido_correcto(self):
        self.assertTrue(es_email_valido("juan@arg.com.ar"))
        self.assertTrue(es_email_valido("admin123@cba.gov.ar"))

    def test_email_valido_sin_arroba(self):
        self.assertFalse(es_email_valido("perezarg.com.ar"))

    def test_email_valido_multiples_arrobas(self):
        self.assertFalse(es_email_valido("test@@arg.com"))

    def test_email_valido_con_espacios(self):
        self.assertFalse(es_email_valido("test @arg.com"))
        self.assertFalse(es_email_valido(" test@arg.com"))

    def test_email_valido_vacio(self):
        self.assertFalse(es_email_valido(""))
