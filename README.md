# Cliente de Correo Electrónico — Proyecto Final  
Grupo 29 — Comisión 2  

## Integrantes  
- Mauricio Ramirez  
- Lara Zobaji  

---

## Descripción General

Este proyecto implementa un cliente de correo electrónico orientado a objetos en Python, diseñado para simular el envío, recepción y organización de mensajes entre usuarios y servidores dentro de una red distribuida.  
El sistema integra estructuras de datos avanzadas, recursividad, colas de prioridad, grafos y una interfaz de línea de comandos (CLI), cumpliendo los requerimientos solicitados para la entrega final.

---

## Objetivo del Proyecto

El objetivo principal es desarrollar un sistema que permita:

- Gestionar usuarios, mensajes y carpetas mediante estructuras recursivas.  
- Enviar mensajes a través de una red de servidores modelada como grafo.  
- Manejar mensajes urgentes utilizando una cola de prioridad basada en heapq.  
- Aplicar filtros automáticos mediante listas y diccionarios.  
- Integrar todas las funcionalidades en una interfaz de consola interactiva.

---

## Estructura de Archivos del Proyecto

| Archivo | Descripción |
|--------|-------------|
| **Clases.py** | Contiene ServidorCorreo y Usuario. Gestionan usuarios, mensajes y carpetas. |
| **Objetos.py** | Define Mensaje y Carpeta, con funciones recursivas y de movimiento. |
| **Grafo.py** | Implementa la red de servidores usando algoritmos BFS y DFS. |
| **Interfaces.py** | Interfaces IEnviador, IRecibidor, IListador para mantener coherencia. |
| **Utilidades.py** | Validación de correos y otras utilidades auxiliares. |
| **Main.py** | Punto de entrada del sistema. Ejecuta la CLI. |

---

## Estructuras de Datos Utilizadas

| Estructura | Función |
|-----------|---------|
| **Árbol Recursivo** | Modela la jerarquía de carpetas de cada usuario. |
| **Diccionarios** | Registro de usuarios y subcarpetas. |
| **Cola de Prioridad (heapq)** | Manejo eficiente de mensajes urgentes. |
| **Grafo (BFS / DFS)** | Modelo de red de servidores y rutas de envío. |

---

## Funcionalidades Principales

### Gestión de Mensajes
- Enviar mensajes entre usuarios.  
- Recibir mensajes.  
- Búsqueda por remitente o asunto.  
- Cambiar prioridad.  
- Mover mensajes entre carpetas.  

### Carpetas y Subcarpetas (Árbol Recursivo)
- Creación de subcarpetas.  
- Listado recursivo.  
- Búsqueda recursiva de mensajes.  
- Movimiento de mensajes entre carpetas.  

### Cola de Mensajes Urgentes
- Encolado mediante heapq.  
- Extracción en orden según prioridad.  
- Procesamiento de mensajes pendientes.  

### Red de Servidores (Grafo)
- Conexión entre servidores.  
- Envío de mensajes mediante BFS o DFS.  
- Simulación de rutas entre nodos.  

---

## Instalación y Ejecución

### 1. Clonar el Repositorio
```bash
git clone https://github.com/larazobaji/proyectoEDD.git
cd proyectoEDD
```

### 2. Ejecutar el Programa Principal
```bash
python Main.py
```

### 3. Funcionalidades Disponibles desde la Terminal
- Crear y conectar servidores.  
- Registrar usuarios.  
- Iniciar sesión.  
- Enviar mensajes usando BFS o DFS.  
- Organizar carpetas.  
- Buscar mensajes recursivamente.  
- Procesar mensajes urgentes.  

---

## Funcionamiento Interno del Sistema

| Tarea | Descripción |
|-------|-------------|
| **Búsqueda de carpeta** | Recorrido recursivo de subcarpetas hasta encontrar coincidencia. |
| **Búsqueda de mensaje** | Revisión de mensajes en todas las carpetas y subcarpetas. |
| **Manejo de urgencias** | Uso de heapq para priorizar mensajes urgentes. |
| **Procesamiento de cola** | Desencolado y entrega de mensajes pendientes. |
| **Enrutamiento (BFS/DFS)** | Recorrido completo del grafo de servidores. |

---

## Enlaces del Proyecto

- **Tablero Trello:** https://trello.com/b/UAu9U4Hi  
- **Repositorio GitHub:** https://github.com/larazobaji/proyectoEDD  
