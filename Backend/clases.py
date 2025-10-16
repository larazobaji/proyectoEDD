from __future__ import annotations
from datetime import datetime
import heapq
from typing import List, Optional, Dict
from interfaces import IEnviador, IRecibidor, IListador
from objetos import Mensaje, Carpeta

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

    @property
    def usuarios(self) -> List[Usuario]:
        return list(self._usuarios.values())
        
    def registrar_usuario(self, usuario: Usuario):
        self._usuarios[usuario.email] = usuario
        print(f"Usuario {usuario.nombre_usuario} registrado en el servidor {self._nombre_servidor}.")
        
    def encolar_mensaje(self, mensaje: Mensaje):
        heapq.heappush(self._mensajes_en_espera, mensaje)
        
    def procesar_mensajes(self):
        print(f"\n[Servidor {self._nombre_servidor}] Procesando mensajes...")
        if not self._mensajes_en_espera:
            print(f"[Servidor {self._nombre_servidor}] No hay mensajes en la cola.")
            return

        while self._mensajes_en_espera:
            mensaje_a_entregar = heapq.heappop(self._mensajes_en_espera)
            print(f"[Servidor {self._nombre_servidor}] Entregando: {mensaje_a_entregar.asunto}")
            
            destinatario_email = mensaje_a_entregar.destinatario
            usuario = self._usuarios.get(destinatario_email)
            
            if usuario:
                usuario.recibir_mensaje(mensaje_a_entregar)
            else:
                print(f"[Servidor {self._nombre_servidor}] Error: Destinatario {destinatario_email} no encontrado.")

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
        
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def nombre_usuario(self) -> str:
        return self._nombre
    
    @property
    def id_usuario(self) -> int:
        return self._id
        
    @property
    def carpetas_raiz(self) -> Dict[str, Carpeta]:
        return self._carpetas_raiz
        
    def enviar_mensaje(self, destinatario: str, asunto: str, cuerpo: str):
        mensaje = Mensaje(self.email, destinatario, asunto, cuerpo)
        self._carpetas_raiz["Enviados"].agregar_mensaje(mensaje)
        print(f"[{self.email}] -> Enviado a {destinatario}.")
        return mensaje
        
    def recibir_mensaje(self, mensaje: Mensaje):
        self._carpetas_raiz["Bandeja de Entrada"].agregar_mensaje(mensaje)
        print(f"[{self.email}] <- Recibido de {mensaje.remitente}.")

    def listar_bandeja_entrada(self):
        bandeja = self._carpetas_raiz["Bandeja de Entrada"]
        print(f"\n--- {bandeja.nombre} de {self.nombre_usuario} ---")
        
        mensajes = bandeja.listar_mensajes()
        if not mensajes:
            print("Tu bandeja de entrada está vacía.")
            return
            
        for i, mensaje in enumerate(mensajes, 1):
            print(f"{i}. {mensaje}")

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
        
    def buscar_mensaje_recursivo(self, criterio: str, valor: str) -> List[Mensaje]:
        resultados = []
        for carpeta_raiz in self._carpetas_raiz.values():
            resultados.extend(carpeta_raiz.buscar_mensaje(criterio, valor))
        return resultados

    def iniciar_sesion(self, contraseña_ingresada: str) -> bool:
        return self._contraseña == contraseña_ingresada
