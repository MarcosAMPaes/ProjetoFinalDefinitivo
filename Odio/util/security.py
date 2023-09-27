# /util/security.py
from fastapi import Request


def validar_usuario_logado(request: Request) -> bool:
    try:
        token = request.cookies["auth_token"]
        if (token != "123456"):
            return False
    except KeyError:
        return False
    
    return True

def gerar_token(tamanho: int = 32) -> str:
    return "123456"