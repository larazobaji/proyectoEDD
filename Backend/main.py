from __future__ import annotations
from clases import ServidorCorreo, Usuario
from utilidades import es_email_valido
from objetos import Mensaje, Carpeta, TipoEtiqueta

if __name__ == "__main__":
    print("--- ¡Inicio! ---")
    
    servidor = ServidorCorreo("mi-empresa.com", "ServidorPrincipal")
    
    def registrar_usuario_interactivo(id_usuario: int) -> Usuario:
        print(f"\n--- Registro de Usuario {id_usuario} ---")
        
        while True:
            nombre = input("Ingrese su nombre: ").strip()
            if nombre:
                break
            else:
                print(" Error: El nombre no puede estar vacío. Intente de nuevo.")

        while True:
            email = input("Ingrese su email: ")
            if es_email_valido(email):
                break
            else:
                print(" Mail incorrecto. Debe tener un solo '@' y ningún espacio. Intente de nuevo.")
        
        contraseña = input("Ingrese una contraseña: ")
        
        usuario = Usuario(nombre, email, id_usuario, contraseña)
        servidor.registrar_usuario(usuario)
        return usuario
    
    usuario1 = registrar_usuario_interactivo(1)
    usuario2 = registrar_usuario_interactivo(2)
    
    print("\n--- ¡Inicio de Sesión! ---")

    usuario_encontrado = None
    while usuario_encontrado is None:
        email_ingresado = input("Ingrese su email para iniciar sesión: ")
        for user in servidor.usuarios:
            if user.email == email_ingresado:
                usuario_encontrado = user
                break
        if usuario_encontrado is None:
            print("Error: Usuario no encontrado, intente de nuevo.")

    intentos = 0
    while intentos < 2:
        contraseña_ingresada = input("Ingrese su contraseña: ")
        if usuario_encontrado.iniciar_sesion(contraseña_ingresada):
            print("\n--- ¡Sesión iniciada con éxito! ---")

            while True:
                print("\n--- Menú de Opciones ---")
                print("1. Enviar un correo")
                print("2. Revisar bandeja de entrada")
                print("3. Crear nueva carpeta o subcarpeta")
                print("4. Buscar mensajes (recursivo)")
                print("5. Cerrar sesión")
                
                opcion = input("Ingrese el número de la opción que desea: ")
                
                if opcion == "1":
                    print("\n--- Enviar un Mensaje ---")
                    
                    destinatario_valido = False
                    while not destinatario_valido:
                        destinatario = input("Ingrese el email del destinatario: ")
                        destinatario_valido = any(user.email == destinatario for user in servidor.usuarios)
                        if not destinatario_valido:
                            print(" Error: Destinatario no encontrado en el servidor. Intente de nuevo.")
                    
                    asunto = input("Ingrese el asunto del mensaje: ")
                    cuerpo = input("Ingrese el cuerpo del mensaje: ")
                    
                    mensaje_enviado = usuario_encontrado.enviar_mensaje(destinatario, asunto, cuerpo)
                    
                    es_urgente = input("¿El mensaje es urgente? (si/no): ").lower() == "si"
                    if es_urgente:
                        mensaje_enviado.marcar_como_urgente()
                    
                    servidor.encolar_mensaje(mensaje_enviado)
                    servidor.procesar_mensajes()

                elif opcion == "2":
                    usuario_encontrado.listar_bandeja_entrada()
                    
                elif opcion == "3":
                    print("\n--- Crear Carpeta ---")
                    nombre = input("Ingrese el nombre de la nueva carpeta/subcarpeta: ")
                    padre = input("Ingrese el nombre de la carpeta padre (deje vacío para carpeta raíz): ")
                    usuario_encontrado.crear_carpeta(nombre, padre.strip() if padre.strip() else None)
                    print(f"Carpeta/subcarpeta {nombre} creada.")
                
                elif opcion == "4":
                    print("\n--- Búsqueda Recursiva ---")
                    criterio = input("Buscar por (asunto/remitente): ").lower()
                    if criterio not in ["asunto", "remitente"]:
                        print("Criterio inválido.")
                        continue
                    
                    valor = input(f"Ingrese valor a buscar en {criterio}: ")
                    
                    resultados = usuario_encontrado.buscar_mensaje_recursivo(criterio, valor)
                    
                    print(f"\nResultados encontrados: {len(resultados)}")
                    for i, msg in enumerate(resultados, 1):
                        print(f"{i}. De: {msg.remitente}, Asunto: {msg.asunto}")

                elif opcion == "5":
                    print("¡Sesión cerrada!")
                    break
                else:
                    print(" Opción no válida. Por favor, ingrese un número del 1 al 5.")
            
            break
        else:
            intentos += 1
            if intentos < 2:
                print("\nError: Contraseña incorrecta. Intente de nuevo.")
            else:
                print("\nError: Contraseña incorrecta. Ha excedido el número de intentos.")
                break
