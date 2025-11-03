from __future__ import annotations

def es_email_valido(email: str) -> bool:
    if email.count("@") != 1 or " " in email:
        return False
    return True