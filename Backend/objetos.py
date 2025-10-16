from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict
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
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._cuerpo = cuerpo
        self._fecha = datetime.now()
        self._es_urgente = es_urgente
        self._etiquetas: List[TipoEtiqueta] = [TipoEtiqueta.NORMAL]

    def __lt__(self, other):
        return self.es_urgente > other.es_urgente

    @property
    def asunto(self) -> str:
        return self._asunto
    
    @property
    def remitente(self) -> str:
        return self._remitente
        
    @property
    def destinatario(self) -> str:
        return self._destinatario
    
    @property
    def cuerpo(self) -> str:
        return self._cuerpo
        
    @property
    def es_urgente(self) -> bool:
        return self._es_urgente
    
    def marcar_como_urgente(self):
        self._es_urgente = True
    
    def agregar_etiqueta(self, etiqueta: TipoEtiqueta):
        if etiqueta not in self._etiquetas:
            self._etiquetas.append(etiqueta)

    def __repr__(self):
        etiquetas_str = ", ".join([e.value for e in self._etiquetas])
        return f"Mensaje(De: {self._remitente}, Asunto: '{self._asunto}', Etiquetas: [{etiquetas_str}])"

class Carpeta:
    def __init__(self, nombre: str, padre: Optional[Carpeta] = None):
        self._nombre = nombre
        self._mensajes: List[Mensaje] = []
        self._subcarpetas: Dict[str, Carpeta] = {}
        self._padre = padre
        
    @property
    def nombre(self) -> str:
        return self._nombre
        
    @property
    def mensajes(self) -> List[Mensaje]:
        return self._mensajes
        
    def agregar_mensaje(self, mensaje: Mensaje):
        self._mensajes.append(mensaje)
        
    def listar_mensajes(self) -> List[Mensaje]:
        return self._mensajes

    def agregar_carpeta(self, nombre_subcarpeta: str) -> Optional[Carpeta]:
        if nombre_subcarpeta not in self._subcarpetas:
            nueva_carpeta = Carpeta(nombre_subcarpeta, padre=self)
            self._subcarpetas[nombre_subcarpeta] = nueva_carpeta
            return nueva_carpeta
        return None

    def buscar_carpeta(self, nombre_carpeta: str) -> Optional[Carpeta]:
        if self._nombre == nombre_carpeta:
            return self
            
        for subcarpeta in self._subcarpetas.values():
            encontrada = subcarpeta.buscar_carpeta(nombre_carpeta)
            if encontrada:
                return encontrada
        return None
        
    def buscar_mensaje(self, criterio: str, valor: str) -> List[Mensaje]:
        resultados = []
        
        for mensaje in self._mensajes:
            if criterio.lower() == 'asunto' and valor.lower() in mensaje.asunto.lower():
                resultados.append(mensaje)
            elif criterio.lower() == 'remitente' and valor.lower() in mensaje.remitente.lower():
                resultados.append(mensaje)
        
        for subcarpeta in self._subcarpetas.values():
            resultados.extend(subcarpeta.buscar_mensaje(criterio, valor))
            
        return resultados

    def mover_mensaje(self, mensaje: Mensaje, carpeta_destino: Carpeta) -> bool:
        if mensaje in self._mensajes:
            self._mensajes.remove(mensaje)
            carpeta_destino.agregar_mensaje(mensaje)
            return True
        return False
