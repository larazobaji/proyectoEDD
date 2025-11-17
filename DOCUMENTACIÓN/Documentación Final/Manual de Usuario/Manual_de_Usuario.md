# Manual de Usuario (Intermedio)
## Cliente de Correo Electrónico – Proyecto Final

---

## 1. Introducción
Este manual explica cómo utilizar el sistema “Cliente de Correo Electrónico”, una aplicación en Python que permite enviar, recibir y organizar mensajes entre usuarios y servidores. Está dirigido a cualquier usuario que emplee la interfaz de línea de comandos (CLI).

---

## 2. Requisitos del Sistema
- Python 3.10 o superior  
- Consola o terminal  
- Repositorio clonado desde GitHub  
- Conexión entre servidores configurada dentro del sistema

---

## 3. Instalación

### 3.1 Clonar el repositorio
```bash
git clone https://github.com/larazobaji/proyectoEDD.git
cd proyectoEDD
```

### 3.2 Ejecutar el sistema
```bash
python Main.py
```

---

## 4. Interfaz Principal
Al ejecutar el programa aparece el menú inicial:

```
=== CLIENTE DE CORREO ELECTRÓNICO ===
1. Administrar Servidores
2. Registrar Usuario
3. Iniciar Sesión
0. Salir
```

---

## 5. Servidores

### 5.1 Crear un servidor
Crea un nodo nuevo dentro de la red de servidores.

### 5.2 Conectar servidores
Permite unir servidores mediante una conexión directa, necesaria para el uso de BFS o DFS.

### 5.3 Mostrar red
Muestra todas las conexiones establecidas.

---

## 6. Usuarios

### 6.1 Registrar un usuario
Se solicita:
- Nombre  
- Email válido  
- Servidor donde será creado  

### 6.2 Iniciar sesión
Tras ingresar el email y servidor, aparece el menú del usuario:

```
1. Enviar Mensaje
2. Ver Bandeja de Entrada
3. Carpetas
4. Filtros
5. Mensajes Urgentes
0. Cerrar Sesión
```

---

## 7. Enviar Mensajes
El usuario debe ingresar:
- Email del destinatario  
- Asunto  
- Cuerpo  
- Prioridad (1–5)  
- Método de envío (BFS o DFS)

Si el destinatario está en otro servidor, el sistema buscará una ruta válida.

---

## 8. Bandeja de Entrada
Aquí se muestran todos los mensajes recibidos, permitiendo:
- Leer mensaje  
- Marcar como leído  
- Mover a carpetas  

---

## 9. Carpetas
Los usuarios pueden:
- Crear subcarpetas  
- Mover mensajes  
- Realizar búsquedas recursivas  

La estructura funciona como un árbol general.

---

## 10. Filtros Automáticos
Los filtros permiten mover automáticamente mensajes según:
- Remitente  
- Asunto  
- Palabras clave  

Se pueden crear, editar y eliminar desde el menú.

---

## 11. Mensajes Urgentes
Los mensajes con prioridad 1 pasan a una cola especial donde se procesan antes que los demás.

---

## 12. Solución de Problemas

### No se encuentra un usuario
Verifique:
- Email  
- Servidor correcto  
- Registro previo  

### No se puede enviar mensaje
Revise:
- Prioridad válida  
- Conexión entre servidores  

### No aparecen carpetas
El usuario debe crearlas desde el menú “Carpetas”.

---

## 13. Cierre de Sesión
Volver al menú principal para cambiar de usuario o finalizar el programa.

