# Cliente de Correo Electrónico — Grupo 29, Comisión 2

**Integrantes:**  
- Mauricio Ramirez  
- Lara Zobaji  

---

## Objetivo del Proyecto

El objetivo principal es **diseñar e implementar un sistema de cliente de correo electrónico orientado a objetos en Python**, que permita simular el envío y recepción de mensajes entre usuarios y servidores.  

El desarrollo se centra en aplicar principios de **encapsulamiento, modularización y estructuras de datos avanzadas**, creando un sistema eficiente, extensible y fácil de mantener.

---

## Estructura del Proyecto

| Archivo | Descripción |
|----------|--------------|
| **Clases.py** | Contiene las clases principales `ServidorCorreo` y `Usuario`. Gestionan usuarios, mensajes y la jerarquía de carpetas. |
| **Objetos.py** | Define los objetos base del sistema: `Mensaje` y `Carpeta`. Incluye búsqueda recursiva y movimientos entre carpetas. |
| **Grafo.py** | Implementa la red de servidores (`RedServidores`) y los métodos BFS/DFS para simular el envío de correos entre nodos. |
| **Interfaces.py** | Define las interfaces abstractas (`IEnviador`, `IRecibidor`, `IListador`) que garantizan coherencia entre clases. |
| **Utilidades.py** | Contiene funciones auxiliares, como la validación de correos electrónicos. |
| **Main.py** | Archivo principal que ejecuta la simulación interactiva del sistema. Permite crear servidores, usuarios y enviar correos. |

---

## Estructuras de Datos Utilizadas

| Estructura | Aplicación |
|-------------|-------------|
| **Árbol (Recursividad)** | Representa la jerarquía de carpetas y subcarpetas dentro de cada usuario. Permite búsquedas recursivas de mensajes. |
| **Diccionarios** | Utilizados para registrar usuarios por email dentro del servidor y organizar subcarpetas por nombre. |
| **Cola de Prioridades (`heapq`)** | Administra los mensajes en espera de envío, priorizando aquellos marcados como **urgentes**. |
| **Grafo (BFS / DFS)** | Modela la conexión entre servidores, permitiendo simular el recorrido de un mensaje a través de la red. |

---

## Ejecución del Proyecto

### 1- Clonar el Repositorio
```bash
git clone https://github.com/larazobaji/proyectoEDD.git
cd proyectoEDD
```

### 2- Ejecutar el Programa Principal
```bash
python Main.py
```

### 3- Interacción
Desde la terminal podrás:
- Crear y conectar servidores.  
- Registrar usuarios.  
- Iniciar sesión.  
- Enviar mensajes (con BFS o DFS).  
- Mover correos entre carpetas.  
- Buscar mensajes recursivamente por asunto o remitente.

## Complejidad Temporal — Análisis Breve

| Operación | Descripción |
|------------|--------------|
| **Búsqueda recursiva de carpeta** | Recorre todas las subcarpetas hasta encontrar la coincidencia. |
| **Búsqueda de mensaje** | Recorre todos los mensajes en cada carpeta y subcarpeta. |
| **Encolado de mensajes urgentes** | Uso de `heapq` para mantener la prioridad. |
| **Procesamiento de cola** | Desencolado y entrega de todos los mensajes pendientes. |
| **BFS / DFS en grafo de servidores** | Recorrido completo de la red según el método elegido. |

---

## Enlaces Importantes
- **Trello (Gestión del Proyecto):** https://trello.com/b/UAu9U4Hi
- **Repositorio GitHub:** https://github.com/larazobaji/proyectoEDD
