from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from objetos import Mensaje

class IEnviador(ABC):
    @abstractmethod
    def enviar_mensaje(self, destinatario: str, asunto: str, cuerpo: str):
        pass

class IRecibidor(ABC):
    @abstractmethod
    def recibir_mensaje(self, mensaje: Mensaje):
        pass

class IListador(ABC):
    @abstractmethod
    def listar_mensajes(self) -> List[Mensaje]:
        pass
