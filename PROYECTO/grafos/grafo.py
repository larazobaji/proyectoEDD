from __future__ import annotations
from typing import Dict, List, Optional, Set
from collections import deque

class RedServidores:
    def __init__(self):
        self._nodos: Dict[str, object] = {}
        self._adyacencia: Dict[str, Set[str]] = {}

    def agregar_servidor(self, nombre: str, servidor_obj: object):
        if nombre in self._nodos:
            return
        self._nodos[nombre] = servidor_obj
        self._adyacencia[nombre] = set()

    def conectar(self, nombre_a: str, nombre_b: str):
        if nombre_a not in self._nodos or nombre_b not in self._nodos:
            return
        self._adyacencia[nombre_a].add(nombre_b)
        self._adyacencia[nombre_b].add(nombre_a)

    def obtener_servidor(self, nombre: str) -> Optional[object]:
        return self._nodos.get(nombre)

    def bfs_ruta(self, origen: str, destino: str) -> Optional[List[str]]:
        if origen not in self._nodos or destino not in self._nodos:
            return None
        cola = deque([origen])
        visitado: Set[str] = {origen}
        padre: Dict[str, Optional[str]] = {origen: None}

        while cola:
            actual = cola.popleft()
            if actual == destino:
                break
            for vecino in self._adyacencia.get(actual, []):
                if vecino not in visitado:
                    visitado.add(vecino)
                    padre[vecino] = actual
                    cola.append(vecino)

        if destino not in padre:
            return None

        ruta: List[str] = []
        nodo = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = padre.get(nodo)
        ruta.reverse()
        return ruta

    def dfs_ruta(self, origen: str, destino: str) -> Optional[List[str]]:
        if origen not in self._nodos or destino not in self._nodos:
            return None
        pila = [(origen, None)]
        padre: Dict[str, Optional[str]] = {}
        visitado: Set[str] = set()

        while pila:
            actual, _ = pila.pop()
            if actual in visitado:
                continue
            visitado.add(actual)
            if actual == origen and actual not in padre:
                padre[actual] = None
            if actual == destino:
                break
            for vecino in self._adyacencia.get(actual, []):
                if vecino not in visitado:
                    padre[vecino] = actual
                    pila.append((vecino, actual))

        if destino not in padre:
            return None

        ruta: List[str] = []
        nodo = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = padre.get(nodo)
        ruta.reverse()
        return ruta

    def simular_envio(self, mensaje, nombre_origen: str, nombre_destino: str, metodo: str = "bfs") -> Optional[List[str]]:
        if metodo.lower() == "bfs":
            ruta = self.bfs_ruta(nombre_origen, nombre_destino)
        else:
            ruta = self.dfs_ruta(nombre_origen, nombre_destino)

        if not ruta:
            return None

        for idx, nombre_servidor in enumerate(ruta):
            servidor = self.obtener_servidor(nombre_servidor)
            if servidor is None:
                return None
            servidor.encolar_mensaje(mensaje)
            servidor.procesar_mensajes()
        return ruta