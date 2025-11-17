# Manual Técnico (Intermedio)
## Cliente de Correo Electrónico – Proyecto Final

---

## 1. Introducción
Este manual describe la arquitectura interna, estructuras de datos, clases y algoritmos utilizados en el proyecto “Cliente de Correo Electrónico”. Está dirigido a desarrolladores o docentes que necesiten comprender el funcionamiento técnico del sistema.

---

## 2. Arquitectura General
El sistema está compuesto por:
- **ServidorCorreo**: administra usuarios, conexiones y mensajes.  
- **Usuario**: representa un cliente dentro del sistema.  
- **Mensaje**: entidad base con prioridad, remitente, cuerpo y asunto.  
- **Carpeta**: estructura recursiva para almacenar mensajes.  
- **Grafo de servidores**: nodos conectados para simular rutas.  
- **Cola de prioridad**: heapq para mensajes urgentes.  
- **CLI**: interfaz para interacción del usuario.  

---

## 3. Estructuras de Datos

### 3.1 Árbol (Carpetas)
- Cada carpeta contiene listas de mensajes y subcarpetas.  
- Búsquedas y listados son implementados con recursividad.  
- Complejidad:  
  - Búsqueda: O(n)  
  - Inserción: O(1) con referencia al padre  

### 3.2 Diccionarios
Usados para:
- Usuarios por email  
- Subcarpetas por nombre  

### 3.3 Cola de Prioridad
Implementada con heapq.  
Operaciones:
- Encolar: O(log n)  
- Desencolar: O(log n)

### 3.4 Grafo de servidores
Modelado como lista de adyacencia.  
Incluye BFS y DFS para encontrar rutas.

---

## 4. Principales Clases del Sistema

### 4.1 Usuario
Responsabilidades:
- Enviar y recibir mensajes  
- Crear carpetas  
- Aplicar filtros  
- Buscar mensajes  

Atributos relevantes:
- Nombre  
- Email  
- Carpeta principal  
- Carpeta de enviados  

### 4.2 ServidorCorreo
Responsabilidades:
- Registrar usuarios  
- Recibir mensajes  
- Enviar mensajes locales o remotos  
- Conectar servidores  

Incluye:
- ColaPrioridad  
- Lista de conexiones  

### 4.3 Mensaje
Atributos:
- Remitente  
- Destinatario  
- Asunto  
- Cuerpo  
- Fecha  
- Prioridad  
- Etiquetas  

### 4.4 Carpeta
Métodos principales:
- agregar_mensaje()  
- mover_mensaje()  
- buscar_mensaje_recursivo()  
- listar_subcarpetas()  

---

## 5. Algoritmos Implementados

### 5.1 Recursividad
Usada para:
- Búsqueda de mensajes  
- Listado de carpetas  
- Movimiento de nodos  

### 5.2 BFS y DFS
Utilizados para:
- Enviar mensajes entre servidores  
- Encontrar rutas  
- Verificar conectividad  

Complejidad:
- O(V + E)

### 5.3 Manipulación de heapq
Para mensajes urgentes.  
Métodos:
- heappush  
- heappop  

---

## 6. Diseño Orientado a Objetos

Principios aplicados:
- Encapsulamiento en todas las clases  
- División modular del código  
- Separación de responsabilidades  
- Interfaces para estandarizar métodos  

---

## 7. Extensibilidad

Posibles mejoras:
- Implementar autenticación  
- Mensajes cifrados  
- Interfaz gráfica  
- Uso de hilos para envío asincrónico  

---

## 8. Pruebas
El sistema incluye pruebas unitarias para:
- Usuario  
- Carpeta  
- Grafo  
- Cola de prioridad  

Recomendación:
```bash
python -m pytest tests/
```
