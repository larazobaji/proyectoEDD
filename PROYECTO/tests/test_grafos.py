import unittest
from collections import deque
from unittest.mock import MagicMock, patch
from grafos.grafo import RedServidores


class MockServidor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mensajes_recibidos = []

    def encolar_mensaje(self, mensaje):
        self.mensajes_recibidos.append(mensaje)

    def procesar_mensajes(self):
        pass

    def __repr__(self):
        return f"MockServidor({self.nombre})"


class TestRedServidores(unittest.TestCase):
    def setUp(self):
        self.red = RedServidores()
        self.s_bsas = MockServidor("BuenosAires")
        self.s_cordoba = MockServidor("Cordoba")
        self.s_mendoza = MockServidor("Mendoza")
        self.s_salta = MockServidor("Salta")

        self.red.agregar_servidor("BuenosAires", self.s_bsas)
        self.red.agregar_servidor("Cordoba", self.s_cordoba)
        self.red.agregar_servidor("Mendoza", self.s_mendoza)

        self.red.conectar("BuenosAires", "Cordoba")
        self.red.conectar("Cordoba", "Mendoza")

    def test_agregar_servidor(self):
        self.assertIn("BuenosAires", self.red._nodos)

    def test_conectar(self):
        self.assertIn("Cordoba", self.red._adyacencia["BuenosAires"])
        self.assertIn("BuenosAires", self.red._adyacencia["Cordoba"])
        self.red.conectar("BuenosAires", "Salta")
        self.assertNotIn("Salta", self.red._adyacencia["BuenosAires"])

    def test_bfs_ruta_existente(self):
        ruta = self.red.bfs_ruta("BuenosAires", "Mendoza")
        self.assertEqual(ruta, ["BuenosAires", "Cordoba", "Mendoza"])

    def test_bfs_ruta_no_existente(self):
        self.red.agregar_servidor("Salta", self.s_salta)
        ruta = self.red.bfs_ruta("BuenosAires", "Salta")
        self.assertIsNone(ruta)

    def test_dfs_ruta_existente(self):
        ruta = self.red.dfs_ruta("BuenosAires", "Mendoza")
        self.assertEqual(ruta, ["BuenosAires", "Cordoba", "Mendoza"])

    def test_simular_envio_bfs(self):
        mensaje_mock = MagicMock()
        ruta = self.red.simular_envio(
            mensaje_mock, "BuenosAires", "Mendoza", metodo="bfs")

        self.assertIsNotNone(ruta)
        self.assertIn(mensaje_mock, self.s_bsas.mensajes_recibidos)

    def test_simular_envio_dfs(self):
        mensaje_mock = MagicMock()
        ruta = self.red.simular_envio(
            mensaje_mock, "BuenosAires", "Mendoza", metodo="dfs")

        self.assertIsNotNone(ruta)
        self.assertIn(mensaje_mock, self.s_bsas.mensajes_recibidos)

    def test_simular_envio_sin_ruta(self):
        mensaje_mock = MagicMock()
        self.red.agregar_servidor("Salta", self.s_salta)
        ruta = self.red.simular_envio(mensaje_mock, "BuenosAires", "Salta")

        self.assertIsNone(ruta)
        self.assertEqual(len(self.s_bsas.mensajes_recibidos), 0)
