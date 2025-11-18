from dominio.clases import ServidorCorreo, Usuario
from util.utilidades import es_email_valido
from modelos.objetos import Mensaje
from grafos.grafo import RedServidores


def registrar_usuario_interactivo(id_usuario: int, servidor: ServidorCorreo) -> Usuario:
    print(f"\n--- Registro de Usuario {id_usuario} ---")
    while True:
        nombre = input("Ingrese su nombre: ").strip()
        if nombre:
            break
        else:
            print("Error: El nombre no puede estar vacío. Intente de nuevo.")
    while True:
        email = input("Ingrese su email: ").strip()
        if es_email_valido(email):
            break
        else:
            print(
                "Mail incorrecto. Debe tener un solo '@' y ningún espacio. Intente de nuevo.")
    contraseña = input("Ingrese una contraseña: ")
    usuario = Usuario(nombre, email, id_usuario, contraseña)
    servidor.registrar_usuario(usuario)
    return usuario


def self_mover_mensaje(usuario: Usuario):
    usuario.listar_bandeja_entrada()
    mensajes = usuario.listar_mensajes()
    if not mensajes:
        print("No hay mensajes para mover.")
        return
    try:
        idx = int(input("Ingrese el número del mensaje que desea mover: ")) - 1
        if 0 <= idx < len(mensajes):
            mensaje_a_mover = mensajes[idx]
            origen = "Bandeja de Entrada"
            destino = input("Ingrese el nombre de la carpeta destino: ")
            moved = usuario.mover_mensaje(mensaje_a_mover, origen, destino)
            if moved:
                print("Mensaje movido con éxito.")
            else:
                print("No se pudo mover el mensaje. Verifique la carpeta destino.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")


def self_buscar_mensaje(usuario: Usuario):
    print("\n--- Búsqueda Recursiva ---")
    criterio = input("Ingrese asunto o remitente a buscar: ").strip()
    resultados = usuario.buscar_mensaje_recursivo(criterio)
    if resultados:
        print("\nMensajes encontrados:")
        for i, m in enumerate(resultados, 1):
            print(f"{i}. {m}")
    else:
        print("No se encontraron mensajes con ese criterio.")


if __name__ == "__main__":
    print("--- Inicio del Sistema de Correo ---")
    red = RedServidores()
    servidores = {}
A
    while True:
        print("\n--- Configuración de Servidores ---")
        print("1. Crear nuevo servidor")
        print("2. Conectar servidores")
        print("3. Listar servidores creados")
        print("4. Continuar al registro de usuarios")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del servidor: ").strip()
            dominio = input("Dominio (ej. ejemplo.com): ").strip()
            if nombre not in servidores:
                servidor = ServidorCorreo(dominio, nombre)
                servidores[nombre] = servidor
                red.agregar_servidor(nombre, servidor)
                print(f"Servidor '{nombre}' creado y agregado a la red.")
            else:
                print("Ese nombre ya está en uso.")

        elif opcion == "2":
            s1 = input("Servidor origen: ").strip()
            s2 = input("Servidor destino: ").strip()
            if s1 in servidores and s2 in servidores:
                red.conectar(s1, s2)
                print(f"Servidores '{s1}' y '{s2}' conectados.")
            else:
                print("Uno o ambos servidores no existen.")

        elif opcion == "3":
            if not servidores:
                print("No hay servidores creados aún.")
            else:
                print("Servidores en la red:")
                for s in servidores:
                    print("-", s)

        elif opcion == "4":
            break

        else:
            print("Opción no válida.")

    if not servidores:
        print("Debe crear al menos un servidor para continuar.")
        exit()

    lista_servidores = list(servidores.values())
    servidor_principal = lista_servidores[0]

    print("\n--- REGISTRO DE USUARIOS ---")
    registrar_usuario_interactivo(1, servidor_principal)
    registrar_usuario_interactivo(2, servidor_principal)

    print("\n--- Sistema de Inicio de Sesión ---")

    while True:
        usuario_encontrado = None

        print("\n--- Iniciar Sesión ---")
        while usuario_encontrado is None:
            email = input("Email: ").strip()
            for s in lista_servidores:
                for user in s.obtener_usuarios():
                    if user.obtener_email() == email:
                        usuario_encontrado = user
                        servidor_actual = s
                        break
            if usuario_encontrado is None:
                print("Usuario no encontrado. Intente nuevamente.")

        intentos = 0
        while intentos < 3:
            contraseña = input("Contraseña: ")
            if usuario_encontrado.iniciar_sesion(contraseña):
                print(
                    f"\n--- Sesión iniciada como {usuario_encontrado.obtener_email()} ---")

                while True:
                    print("\n--- Menú ---")
                    print("1. Enviar correo (BFS)")
                    print("2. Enviar correo (DFS)")
                    print("3. Revisar bandeja de entrada")
                    print("4. Mover mensaje")
                    print("5. Buscar mensaje")
                    print("6. Cerrar sesión")
                    op = input("Opción: ")

                    if op in ["1", "2"]:
                        metodo = "bfs" if op == "1" else "dfs"
                        destinatario = input("Email destinatario: ").strip()
                        asunto = input("Asunto: ")
                        cuerpo = input("Cuerpo: ")
                        urgente = input("¿Urgente? (si/no): ").lower() == "si"

                        mensaje = usuario_encontrado.enviar_mensaje(
                            destinatario, asunto, cuerpo, urgente
                        )

                        # *** FIX: el mensaje ahora pasa al servidor ***
                        servidor_actual.encolar_mensaje(mensaje)
                        servidor_actual.procesar_mensajes()

                        servidor_origen = None
                        servidor_destino = None
                        for nombre, s in servidores.items():
                            if usuario_encontrado.obtener_email() in s._usuarios:
                                servidor_origen = nombre
                            for user in s.obtener_usuarios():
                                if user.obtener_email() == destinatario:
                                    servidor_destino = nombre

                        if servidor_origen and servidor_destino:
                            ruta = red.simular_envio(
                                mensaje, servidor_origen, servidor_destino, metodo=metodo)
                            if ruta:
                                print("Mensaje transmitido por ruta:",
                                      " -> ".join(ruta))
                            else:
                                print("No existe conexión entre los servidores.")
                        else:
                            print("Error al determinar servidores de envío.")

                    elif op == "3":
                        usuario_encontrado.listar_bandeja_entrada()

                    elif op == "4":
                        self_mover_mensaje(usuario_encontrado)

                    elif op == "5":
                        self_buscar_mensaje(usuario_encontrado)

                    elif op == "6":
                        print(
                            "\nSesión cerrada. Volviendo al menú de inicio de sesión…")
                        break

                    else:
                        print("Opción no válida.")

                break
            else:
                intentos += 1
                print("Contraseña incorrecta.")
                if intentos == 3:
                    print("Demasiados intentos. Regresando al login.")
