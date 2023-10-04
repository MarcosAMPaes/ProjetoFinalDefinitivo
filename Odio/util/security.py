# /util/security.py
import secrets
import bcrypt
from fastapi import Request
from models.Cliente import Cliente
from Repositories.ClienteRepo import ClienteRepo

def validar_usuario_logado(request: Request) -> Cliente | None:
    try:
        token = request.cookies["auth_token"]
        if token.strip() == "":
            return False
        cliente = ClienteRepo.obterClientePorToken(token)
        return cliente
    except KeyError:
        return False   

def obter_hash_senha(senha: str) -> str:
    # A função bcrypt.hashpw espera que a senha seja em bytes, por isso usamos .encode()
    hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    return hashed.decode()  # Decodificar para obter a string do hash
def verificar_senha(senha: str, hash_senha: str) -> bool:
    try:
        # Certifique-se de que ambos sejam bytes
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False
    
def gerar_token(length: int = 32) -> str:
    return secrets.token_hex(length)