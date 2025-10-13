# Trabajo Final: Cliente de Correo Electrónico

## Grupo y Comisión
* **Integrantes:** Mauricio Ramirez, Lara Zobaji
* **Grupo:** 29
* **Comisión:** 2

## Resumen del Proyecto:
El objetivo principal es diseñar e implementar un sistema de cliente de correo electrónico orientado a objetos utilizando Python. El sistema modela la gestión de usuarios, el flujo de mensajes entre servidores, y la organización jerárquica de correos.

El desarrollo se enfoca en la aplicación eficiente de las estructuras de datos avanzadas y el **encapsulamiento**.

## Estructuras de Datos Clave Implementadas

| Estructura | Aplicación en el Proyecto | Función Principal |
| :--- | :--- | :--- |
| **Árbol General (Recursividad)** | Estructura principal para modelar la jerarquía de carpetas y subcarpetas (`Carpeta`). | Permite la organización jerárquica y soporta búsquedas recursivas en todo el sistema de carpetas. |
| **Diccionarios** | Utilizados para el registro de usuarios en el servidor y la gestión interna de subcarpetas por nombre. | Facilita el acceso y la gestión de elementos clave en tiempo $O(1)$. |
| **Cola de Prioridades (Heapq)** | Implementada para gestionar los mensajes en espera, priorizando el envío de los correos marcados como "urgentes". | Asegura que los mensajes críticos sean procesados de forma eficiente y prioritaria. |


## Enlaces Importantes
* **Tablero Trello (Gestión del Proyecto):** https://trello.com/invite/b/68cafb440dcbdc871467b878/ATTIdafaac1d4c090cb93c3ee9d132bfffa291D3726B/estructura-de-datos-tp
* **Repositorio GitHub:** https://github.com/larazobaji/proyectoEDD

## Uso e Inicio
Para ejecutar la simulación del cliente de correo:

1.  Clonar este repositorio.
2.  Ejecutar el archivo principal: `main.py`
