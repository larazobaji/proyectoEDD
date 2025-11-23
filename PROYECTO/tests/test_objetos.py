import unittest
from datetime import datetime

# Ruta de importación corregida
from modelos.objetos import Mensaje, Carpeta, TipoEtiqueta


class TestMensaje(unittest.TestCase):
    def setUp(self):
        self.mensaje = Mensaje(
            "ana@gcorreo.ar", "matias@gcorreo.ar", "Asunto Expediente", "Cuerpo Detalle", False)

    def test_inicializacion(self):
        self.assertEqual(self.mensaje.remitente, "ana@gcorreo.ar")
        self.assertEqual(self.mensaje.asunto, "Asunto Expediente")
        self.assertFalse(self.mensaje.es_urgente)
        self.assertIn(TipoEtiqueta.NORMAL, self.mensaje._etiquetas)

    def test_propiedades(self):
        self.assertEqual(self.mensaje.cuerpo, "Cuerpo Detalle")

    def test_marcar_como_urgente(self):
        self.mensaje.marcar_como_urgente()
        self.assertTrue(self.mensaje.es_urgente)

    def test_agregar_etiqueta(self):
        self.mensaje.agregar_etiqueta(TipoEtiqueta.SPAM)
        self.assertIn(TipoEtiqueta.SPAM, self.mensaje._etiquetas)

    def test_orden_prioridad(self):
        urgente = Mensaje("a", "b", "u", "c", True)
        normal = Mensaje("a", "b", "n", "c", False)

        self.assertTrue(urgente < normal)


class TestCarpeta(unittest.TestCase):
    def setUp(self):
        self.carpeta_raiz = Carpeta("Recibidos_AR")
        self.mensaje1 = Mensaje(
            "cliente@ar.com", "user@gcorreo.ar", "Factura", "Detalle de compra")
        self.mensaje2 = Mensaje(
            "contacto@arg.com.ar", "user@gcorreo.ar", "Consulta", "Duda sobre el trámite")

    def test_inicializacion(self):
        self.assertEqual(self.carpeta_raiz.nombre, "Recibidos_AR")
        self.assertEqual(len(self.carpeta_raiz.mensajes), 0)

    def test_agregar_mensaje_y_listar(self):
        self.carpeta_raiz.agregar_mensaje(self.mensaje1)
        self.assertEqual(len(self.carpeta_raiz.listar_mensajes()), 1)

    def test_agregar_carpeta(self):
        subcarpeta = self.carpeta_raiz.agregar_carpeta("Proyectos_CABA")
        self.assertIsNotNone(subcarpeta)
        self.assertIsNone(self.carpeta_raiz.agregar_carpeta("Proyectos_CABA"))

    def test_buscar_carpeta(self):
        self.carpeta_raiz.agregar_carpeta("Enero").agregar_carpeta("Febrero")

        self.assertEqual(self.carpeta_raiz.buscar_carpeta(
            "Recibidos_AR"), self.carpeta_raiz)
        self.assertIsNotNone(self.carpeta_raiz.buscar_carpeta("Febrero"))

    def test_buscar_mensaje_recursivo(self):
        self.carpeta_raiz.agregar_mensaje(self.mensaje1)
        subcarpeta = self.carpeta_raiz.agregar_carpeta("Archivados_Viejos")
        subcarpeta.agregar_mensaje(self.mensaje2)

        resultados_factura = self.carpeta_raiz.buscar_mensaje("Factura")
        self.assertEqual(len(resultados_factura), 1)

        resultados_contacto = self.carpeta_raiz.buscar_mensaje(
            "contacto@arg.com.ar")
        self.assertEqual(len(resultados_contacto), 1)

    def test_mover_mensaje(self):
        carpeta_destino = Carpeta("Tramites_Finalizados")
        self.carpeta_raiz.agregar_mensaje(self.mensaje1)

        moved = self.carpeta_raiz.mover_mensaje(self.mensaje1, carpeta_destino)
        self.assertTrue(moved)
        self.assertEqual(len(self.carpeta_raiz.mensajes), 0)
