from __future__ import annotations
from datetime import datetime
from typing import List
from enum import Enum

#Clases para Etiquetas

class TipoEtiqueta(Enum):
    NORMAL = "Normal"
    SPAM = "Spam"
    IMPORTANTE = "Importante"
    DESTACADO = "Destacado"

#Clases para Mensaje y Carpeta

class Mensaje:
    def __init__(self, remitente: str, destinatario: str, asunto: str, cuerpo: str, es_urgente: bool = False):
        self.__remitente = remitente
        self.__destinatario = destinatario
        self.__asunto = asunto
        self.__cuerpo = cuerpo
        self.__fecha = datetime.now()
        self.__es_urgente = es_urgente
        self.__etiquetas: List[TipoEtiqueta] = [TipoEtiqueta.NORMAL]

    def __lt__(self, other):
        return self.es_urgente() > other.es_urgente()

    def obtener_asunto(self) -> str:
        return self.__asunto
    
    def obtener_remitente(self) -> str:
        return self.__remitente
        
    def obtener_destinatario(self) -> str:
        return self.__destinatario
    
    def es_urgente(self) -> bool:
        return self.__es_urgente
    
    def marcar_como_urgente(self):
        self.__es_urgente = True
    
    def agregar_etiqueta(self, etiqueta: TipoEtiqueta):
        if etiqueta not in self.__etiquetas:
            self.__etiquetas.append(etiqueta)

    def __repr__(self):
        etiquetas_str = ", ".join([e.value for e in self.__etiquetas])
        return f"Mensaje(De: {self.__remitente}, Asunto: '{self.__asunto}', Etiquetas: [{etiquetas_str}])"

class Carpeta:
    def __init__(self, nombre: str):
        self.__nombre = nombre
        self.__mensajes: List[Mensaje] = []
        self.__subcarpetas: List[Carpeta] = []
        
    def obtener_nombre(self) -> str:
        return self.__nombre
        
    def agregar_mensaje(self, mensaje: Mensaje):
        self.__mensajes.append(mensaje)
        
    def listar_mensajes(self) -> List[Mensaje]:
        return self.__mensajes
        
    #Busca y elimina un mensaje de la carpeta actual    
    def eliminar_mensaje(self, mensaje: Mensaje) -> bool:
        if mensaje in self.__mensajes:
            self.__mensajes.remove(mensaje)
            return True
        return False
    #Permite añadir una subcarpeta   
    def agregar_subcarpeta(self, carpeta: Carpeta):
        self.__subcarpetas.append(carpeta)
    #Busca mensajes por asunto o remitente de forma recursiva   
    def buscar_mensaje(self, criterio: str) -> List[Mensaje]:
        criterio_lower = criterio.lower()
        mensajes_encontrados = []
        for mensaje in self.__mensajes:
            if criterio_lower in mensaje.obtener_asunto().lower() or \
               criterio_lower in mensaje.obtener_remitente().lower():
                mensajes_encontrados.append(mensaje)
        for subcarpeta in self.__subcarpetas:
            mensajes_encontrados.extend(subcarpeta.buscar_mensaje(criterio))
        return mensajes_encontrados    
