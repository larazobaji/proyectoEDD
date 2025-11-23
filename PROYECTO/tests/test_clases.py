import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from dominio.clases import ServidorCorreo, Usuario
from modelos.objetos import Mensaje, TipoEtiqueta, Carpeta
from dominio.interfaces import IEnviador, IRecibidor, IListador


class TestServidorCorreo(unittest.TestCase):
    def setUp(self):
        self.servidor = ServidorCorreo("gcorreo.ar", "SrvBA")
        self.usuario = Usuario("Julián", "julian@gcorreo.ar", 1, "clave456")
        self.servidor.registrar_usuario(self.usuario)
        self.mensaje_urgente = Mensaje(
            "proveedor@exterior.com", "julian@gcorreo.ar", "Pedido URGENTE de stock", "Necesitamos confirmar la mercadería", True)
        self.mensaje_spam = Mensaje(
            "sorteos@falsos.ar", "julian@gcorreo.ar", "Ganaste un Viaje a Cataratas", "¡Felicidades, tienes un premio!", False)
        self.mensaje_destacado = Mensaje(
            "pago@banco.com.ar", "julian@gcorreo.ar", "¿Se efectuó el débito?", "Una consulta importante.", False)
        self.mensaje_normal = Mensaje(
            "vecino@ar.com", "julian@gcorreo.ar", "Hola, cómo va", "Te escribo por el asado.", False)

    def test_registro_usuario(self):
        self.assertEqual(len(self.servidor.obtener_usuarios()), 1)
        self.assertEqual(
            self.servidor._usuarios["julian@gcorreo.ar"], self.usuario)

    def test_encolar_mensaje(self):
        self.servidor.encolar_mensaje(self.mensaje_normal)
        self.assertEqual(len(self.servidor._mensajes_en_espera), 1)
        self.assertEqual(
            self.servidor._mensajes_en_espera[0], self.mensaje_normal)

    def test_aplicar_filtros_automaticos_spam(self):
        self.servidor._aplicar_filtros_automaticos(self.mensaje_spam)
        self.assertIn(TipoEtiqueta.SPAM, self.mensaje_spam._etiquetas)

    def test_aplicar_filtros_automaticos_urgente(self):
        self.servidor._aplicar_filtros_automaticos(self.mensaje_urgente)
        self.assertIn(TipoEtiqueta.IMPORTANTE, self.mensaje_urgente._etiquetas)

    def test_aplicar_filtros_automaticos_destacado(self):
        self.servidor._aplicar_filtros_automaticos(self.mensaje_destacado)
        self.assertIn(TipoEtiqueta.DESTACADO,
                      self.mensaje_destacado._etiquetas)

    @patch.object(Usuario, 'recibir_mensaje')
    def test_procesar_mensajes_entrega_orden_prioridad(self, mock_recibir):
        self.servidor.encolar_mensaje(self.mensaje_normal)
        self.servidor.encolar_mensaje(self.mensaje_urgente)

        self.servidor.procesar_mensajes()

        llamadas = mock_recibir.call_args_list
        self.assertEqual(llamadas[0][0][0], self.mensaje_urgente)
        self.assertEqual(llamadas[1][0][0], self.mensaje_normal)

    def test_procesar_mensajes_destinatario_no_encontrado(self):
        mensaje_desconocido = Mensaje(
            "a@a.com", "desconocido@gcorreo.ar", "Test", "Msg", False)
        self.servidor.encolar_mensaje(mensaje_desconocido)

        with patch('builtins.print'):
            self.servidor.procesar_mensajes()

    def test_procesar_mensajes_vacios(self):
        with patch('builtins.print') as mock_print:
            self.servidor.procesar_mensajes()
            self.assertTrue(any("[Servidor SrvBA] No hay mensajes en la cola." in call[0][0]
                            for call in mock_print.call_args_list))


class TestUsuario(unittest.TestCase):
    def setUp(self):
        self.usuario = Usuario("Sofía", "sofia@gcorreo.ar", 2, "arg2024")

    def test_implementacion_interfaces(self):
        self.assertIsInstance(self.usuario, IEnviador)
        self.assertIsInstance(self.usuario, IRecibidor)
        self.assertIsInstance(self.usuario, IListador)

    def test_obtener_atributos(self):
        self.assertEqual(self.usuario.obtener_email(), "sofia@gcorreo.ar")

    def test_enviar_mensaje(self):
        mensaje = self.usuario.enviar_mensaje(
            "julian@gcorreo.ar", "Juntada", "Asado este finde")
        self.assertEqual(mensaje.remitente, "sofia@gcorreo.ar")
        self.assertEqual(
            len(self.usuario._carpetas_raiz["Enviados"].listar_mensajes()), 1)

    def test_recibir_mensaje(self):
        mensaje = Mensaje("julian@gcorreo.ar", "sofia@gcorreo.ar",
                          "Ok, nos vemos", "Mensaje de confirmación")
        self.usuario.recibir_mensaje(mensaje)
        self.assertEqual(
            len(self.usuario._carpetas_raiz["Bandeja de Entrada"].listar_mensajes()), 1)

    def test_crear_carpeta_raiz(self):
        self.usuario.crear_carpeta("Personal")
        self.assertIn("Personal", self.usuario._carpetas_raiz)

    def test_crear_subcarpeta(self):
        self.usuario.crear_carpeta("Clientes_BA", "Bandeja de Entrada")
        bandeja = self.usuario._carpetas_raiz["Bandeja de Entrada"]
        self.assertIn("Clientes_BA", bandeja._subcarpetas)

    def test_mover_mensaje(self):
        self.usuario.crear_carpeta("Archivados_2024")
        mensaje = Mensaje("a@a.com", "sofia@gcorreo.ar",
                          "Documento", "Importante")
        self.usuario.recibir_mensaje(mensaje)

        moved = self.usuario.mover_mensaje(
            mensaje, "Bandeja de Entrada", "Archivados_2024")
        self.assertTrue(moved)
        self.assertEqual(
            len(self.usuario._carpetas_raiz["Archivados_2024"].listar_mensajes()), 1)

    def test_buscar_carpeta(self):
        self.usuario.crear_carpeta("Proyectos_MarDel", "Bandeja de Entrada")

        encontrada_raiz = self.usuario.buscar_carpeta("Enviados")
        self.assertIsNotNone(encontrada_raiz)

        encontrada_sub = self.usuario.buscar_carpeta("Proyectos_MarDel")
        self.assertIsNotNone(encontrada_sub)

    def test_buscar_mensaje_recursivo(self):
        self.usuario.crear_carpeta("Trabajo")
        self.usuario.crear_carpeta("Proveedores_Cordoba", "Trabajo")

        msg_jefe = Mensaje("gerente@empresa.ar", "sofia@gcorreo.ar",
                           "Reunion de Gerencia", "Importante")
        msg_proveedor = Mensaje("juan@proveedor.com.ar",
                                "sofia@gcorreo.ar", "Cotización Fideos", "Hola")

        self.usuario.recibir_mensaje(msg_jefe)
        self.usuario.mover_mensaje(
            msg_proveedor, "Bandeja de Entrada", "Proveedores_Cordoba")

        resultados_jefe = self.usuario.buscar_mensaje_recursivo(
            "gerente@empresa.ar")
        self.assertEqual(len(resultados_jefe), 1)

    def test_iniciar_sesion(self):
        self.assertTrue(self.usuario.iniciar_sesion("arg2024"))
        self.assertFalse(self.usuario.iniciar_sesion("clave_mala"))
