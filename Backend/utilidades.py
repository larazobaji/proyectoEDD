from __future__ import annotations

def es_email_valido(email: str) -> bool:
    #Verifica si el formato del email es válido (debe tener exactamente un @ y no espacios).
    if email.count("@") != 1 or email.count(" ") > 0:
        return False
    return True
