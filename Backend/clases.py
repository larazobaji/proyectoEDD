from __future__ import annotations
from datetime import datetime
import heapq
from typing import List, Optional
from interfaces import IEnviador, IRecibidor, IListador
from objetos import Mensaje, Carpeta

#Clase Padre

class ServidorCorreo:
    def __init__(self, dominio: str, nombre_servidor: str):
        self.dominio = dominio
        self.nombre_servidor = nombre_servidor
        self.__usuarios: List[Usuario] = []
        self.__mensajes_en_espera: List[Mensaje] = []
        
    def registrar_usuario(self, usuario: Usuario):
        self.__usuarios.append(usuario)
        print(f"Usuario {usuario.obtener_nombre_usuario()} registrado en el servidor {self.nombre_servidor}.")
        
    def encolar_mensaje(self, mensaje: Mensaje):
        heapq.heappush(self.__mensajes_en_espera, mensaje)
        
    def procesar_mensajes(self):
        print(f"\n[Servidor '{self.nombre_servidor}'] Procesando mensajes...")
        if not self.__mensajes_en_espera:
            print("[Servidor '{self.nombre_servidor}'] No hay mensajes en la cola.")
            return

        while self.__mensajes_en_espera:
            mensaje_a_entregar = heapq.heappop(self.__mensajes_en_espera)
            print(f"[Servidor '{self.nombre_servidor}'] Entregando: '{mensaje_a_entregar.obtener_asunto()}'")
            
            destinatario_encontrado = False
            for usuario in self.__usuarios:
                if usuario.obtener_email() == mensaje_a_entregar.obtener_destinatario():
                    usuario.recibir_mensaje(mensaje_a_entregar)
                    destinatario_encontrado = True
                    break
            
            if not destinatario_encontrado:
                print(f"[Servidor '{self.nombre_servidor}'] Error: Destinatario {mensaje_a_entregar.obtener_destinatario()} no encontrado.")

    def obtener_usuarios(self) -> List[Usuario]:
        return self.__usuarios

#Clases Subclases (Heredan de ServidorCorreo)

class Usuario(ServidorCorreo, IEnviador, IRecibidor):
    def __init__(self, nombre: str, email: str, id_usuario: int, dominio_servidor: str, nombre_servidor: str, contraseña: str):
        super().__init__(dominio_servidor, nombre_servidor)
        self.__id = id_usuario
        self.__nombre = nombre
        self.__email = email
        self.__contraseña = contraseña
        self.__fecha_registro = datetime.now()
        self.__bandeja_entrada = Carpeta("Bandeja de Entrada")
        self.__bandeja_salida = Carpeta("Bandeja de Salida")
        self.__carpetas_personalizadas: List[Carpeta] = []
        
    def obtener_email(self) -> str:
        return self.__email
    
    def obtener_nombre_usuario(self) -> str:
        return self.__nombre
        
    def enviar_mensaje(self, destinatario: str, asunto: str, cuerpo: str):
        mensaje = Mensaje(self.obtener_email(), destinatario, asunto, cuerpo)
        self.__bandeja_salida.agregar_mensaje(mensaje)
        print(f"[{self.obtener_email()}] -> Enviado a {destinatario}.")
        return mensaje
        
    def recibir_mensaje(self, mensaje: Mensaje):
        self.__bandeja_entrada.agregar_mensaje(mensaje)
        print(f"[{self.obtener_email()}] <- Recibido de {mensaje.obtener_remitente()}.")

    def listar_bandeja_entrada(self):
        print(f"\n--- Bandeja de Entrada de {self.obtener_nombre_usuario()} ---")
        mensajes = self.__bandeja_entrada.listar_mensajes()
        if not mensajes:
            print("Tu bandeja de entrada está vacía.")
            return
        
        for i, mensaje in enumerate(mensajes, 1):
            print(f"{i}. {mensaje}")

    def crear_carpeta(self, nombre_carpeta: str):
        nueva_carpeta = Carpeta(nombre_carpeta)
        self.__carpetas_personalizadas.append(nueva_carpeta)
        
    def iniciar_sesion(self, contraseña_ingresada: str) -> bool:
        return self.__contraseña == contraseña_ingresada