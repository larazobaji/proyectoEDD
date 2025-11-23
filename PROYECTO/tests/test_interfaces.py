import unittest
from abc import ABC

from dominio.interfaces import IEnviador, IRecibidor, IListador


class TestInterfaces(unittest.TestCase):

    def test_son_clases_abstractas(self):
        self.assertTrue(issubclass(IEnviador, ABC))
        self.assertTrue(issubclass(IRecibidor, ABC))
        self.assertTrue(issubclass(IListador, ABC))

    def test_no_se_pueden_instanciar(self):
        with self.assertRaises(TypeError):
            IListador()
        with self.assertRaises(TypeError):
            IEnviador()
        with self.assertRaises(TypeError):
            IRecibidor()
