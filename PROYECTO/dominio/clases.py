from __future__ import annotations
from datetime import datetime
import heapq
from typing import List, Optional, Dict
from .interfaces import IEnviador, IRecibidor, IListador
from modelos.objetos import Mensaje, Carpeta, TipoEtiqueta, Filtro


class ServidorCorreo:
    def __init__(self, dominio: str, nombre_servidor: str):
        self._dominio = dominio
        self._nombre_servidor = nombre_servidor
        self._usuarios: Dict[str, Usuario] = {}
        self._mensajes_en_espera: List[Mensaje] = []

    @property
    def dominio(self) -> str:
        return self._dominio

    @property
    def nombre_servidor(self) -> str:
        return self._nombre_servidor

    def obtener_usuarios(self) -> List["Usuario"]:
        return list(self._usuarios.values())

    def registrar_usuario(self, usuario: "Usuario"):
        self._usuarios[usuario.obtener_email()] = usuario
        print(
            f"Usuario {usuario.obtener_nombre()} registrado en el servidor {self._nombre_servidor}.")

    def encolar_mensaje(self, mensaje: Mensaje):
        heapq.heappush(self._mensajes_en_espera, mensaje)

    def _aplicar_filtros_basicos(self, mensaje: Mensaje):
        # Filtros básicos del sistema (SPAM, URGENTE, DESTACADO)
        asunto_lower = mensaje.asunto.lower()
        cuerpo_lower = mensaje.cuerpo.lower()
        palabras_spam = ["oferta", "ganaste", "premio", "descuento", "gratis"]

        if any(p in asunto_lower or p in cuerpo_lower for p in palabras_spam):
            if TipoEtiqueta.NORMAL in mensaje._etiquetas:
                mensaje._etiquetas.remove(TipoEtiqueta.NORMAL)
            mensaje.agregar_etiqueta(TipoEtiqueta.SPAM)

        if mensaje.es_urgente:
            mensaje.agregar_etiqueta(TipoEtiqueta.IMPORTANTE)

        if mensaje.asunto.endswith("?"):
            mensaje.agregar_etiqueta(TipoEtiqueta.DESTACADO)

    def procesar_mensajes(self):
        print(f"\n[Servidor {self._nombre_servidor}] Procesando mensajes...")
        if not self._mensajes_en_espera:
            print(
                f"[Servidor {self._nombre_servidor}] No hay mensajes en la cola.")
            return

        while self._mensajes_en_espera:
            mensaje_a_entregar = heapq.heappop(self._mensajes_en_espera)
            self._aplicar_filtros_basicos(mensaje_a_entregar)

            print(
                f"[Servidor {self._nombre_servidor}] Entregando: {mensaje_a_entregar.asunto}")

            destinatario_email = mensaje_a_entregar.destinatario
            usuario = self._usuarios.get(destinatario_email)

            if usuario:
                # APLICAR FILTROS DEL USUARIO ANTES DE RECIBIR
                carpeta_destino = usuario.aplicar_filtros_usuario(
                    mensaje_a_entregar)

                if carpeta_destino:
                    print(
                        f"[{destinatario_email}] Filtro aplicado: Movido a '{carpeta_destino}'")
                    destino = usuario.buscar_carpeta(carpeta_destino)
                    if destino:
                        destino.agregar_mensaje(mensaje_a_entregar)
                    else:
                        # Si la carpeta destino no existe, va a la Bandeja de Entrada por defecto
                        usuario.recibir_mensaje(mensaje_a_entregar)
                else:
                    usuario.recibir_mensaje(mensaje_a_entregar)
            else:
                print(
                    f"[Servidor {self._nombre_servidor}] Error: Destinatario {destinatario_email} no encontrado.")


class Usuario(IEnviador, IRecibidor, IListador):
    def __init__(self, nombre: str, email: str, id_usuario: int, contraseña: str):
        self._id = id_usuario
        self._nombre = nombre
        self._email = email
        self._contraseña = contraseña
        self._fecha_registro = datetime.now()

        self._carpetas_raiz: Dict[str, Carpeta] = {
            "Bandeja de Entrada": Carpeta("Bandeja de Entrada"),
            "Enviados": Carpeta("Enviados")
        }
        self._filtros: Dict[int, Filtro] = {}

    def obtener_email(self) -> str:
        return self._email

    def obtener_nombre(self) -> str:
        return self._nombre

    def obtener_id(self) -> int:
        return self._id

    def obtener_filtros(self) -> Dict[int, Filtro]:
        return self._filtros

    def agregar_filtro(self, filtro: Filtro):
        self._filtros[filtro.id] = filtro

    def eliminar_filtro(self, filtro_id: int) -> bool:
        if filtro_id in self._filtros:
            del self._filtros[filtro_id]
            return True
        return False

    def aplicar_filtros_usuario(self, mensaje: Mensaje) -> Optional[str]:
        """Aplica filtros configurados y retorna el nombre de la carpeta destino si hay coincidencia."""
        for filtro in self._filtros.values():
            if filtro.campo == 'remitente' and filtro.valor in mensaje.remitente.lower():
                return filtro.carpeta_destino
            if filtro.campo == 'asunto' and filtro.valor in mensaje.asunto.lower():
                return filtro.carpeta_destino
        return None

    def enviar_mensaje(self, destinatario: str, asunto: str, cuerpo: str, es_urgente: bool = False) -> Mensaje:
        mensaje = Mensaje(self._email, destinatario,
                          asunto, cuerpo, es_urgente)
        self._carpetas_raiz["Enviados"].agregar_mensaje(mensaje)
        print(f"[{self._email}] -> Enviado a {destinatario}.")
        return mensaje

    def recibir_mensaje(self, mensaje: Mensaje):
        self._carpetas_raiz["Bandeja de Entrada"].agregar_mensaje(mensaje)
        print(f"[{self._email}] <- Recibido de {mensaje.remitente}.")

    def listar_mensajes(self) -> List[Mensaje]:
        return self._carpetas_raiz["Bandeja de Entrada"].listar_mensajes()

    def listar_bandeja_entrada(self):
        bandeja = self._carpetas_raiz["Bandeja de Entrada"]
        print(f"\n--- {bandeja.nombre} de {self._nombre} ---")

        mensajes = bandeja.listar_mensajes()
        if not mensajes:
            print("No tienes correos.")
            return

        for i, mensaje in enumerate(mensajes, 1):
            print(f"\n===== Mensaje {i} =====")
            print(f"De: {mensaje.remitente}")
            print(f"Asunto: {mensaje.asunto}")
            print(f"Fecha: {mensaje._fecha}")
            print(
                f"Etiquetas: {', '.join([e.value for e in mensaje._etiquetas])}")
            print("\n--- Mensaje ---")
            print(mensaje.cuerpo)
            print("===========================")

    def crear_carpeta(self, nombre_carpeta: str, carpeta_padre: Optional[str] = None):
        if carpeta_padre is None or carpeta_padre not in self._carpetas_raiz:
            if nombre_carpeta not in self._carpetas_raiz:
                self._carpetas_raiz[nombre_carpeta] = Carpeta(nombre_carpeta)
            return

        carpeta = self._carpetas_raiz[carpeta_padre]
        carpeta.agregar_carpeta(nombre_carpeta)

    def mover_mensaje(self, mensaje: Mensaje, origen: str, destino: str) -> bool:
        carpeta_origen = self.buscar_carpeta(origen)
        carpeta_destino = self.buscar_carpeta(destino)

        if not carpeta_origen or not carpeta_destino:
            return False

        return carpeta_origen.mover_mensaje(mensaje, carpeta_destino)

    def buscar_carpeta(self, nombre_carpeta: str) -> Optional[Carpeta]:
        for carpeta_raiz in self._carpetas_raiz.values():
            encontrada = carpeta_raiz.buscar_carpeta(nombre_carpeta)
            if encontrada:
                return encontrada
        return None

    def buscar_mensaje_recursivo(self, criterio: str) -> List[Mensaje]:
        resultados = []
        for carpeta_raiz in self._carpetas_raiz.values():
            resultados.extend(carpeta_raiz.buscar_mensaje(criterio))
        return resultados

    def iniciar_sesion(self, contraseña_ingresada: str) -> bool:
        return self._contraseña == contraseña_ingresada
