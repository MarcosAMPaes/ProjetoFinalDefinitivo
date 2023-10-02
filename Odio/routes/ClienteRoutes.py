# routes/MainRoutes.py
from fastapi import APIRouter, Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Repositories.ItemVendaRepo import ItemVendaRepo
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData
# routes/ProjetoRoutes.py
from fastapi import APIRouter, Depends, Form, Path, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from util.security import obter_hash_senha, validar_usuario_logado, verificar_senha
from util.templateFilters import capitalizar_nome_proprio, formatarData
from Repositories.ClienteRepo import ClienteRepo
from util.validators import *
from models.Cliente import Cliente
from models.Usuario import Usuario


router = APIRouter()

app = FastAPI()

templates = Jinja2Templates(directory="templates")



@router.get('/carrinho', response_class=HTMLResponse)
async def root(request: Request):
    carrinho = ItemVendaRepo.obterTodos()
    return templates.TemplateResponse("carrinho.html", {"request": request, 'carrinho': carrinho})

@router.get('/cadastrarnovasenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cadastrarnovasenha.html", {"request": request,})

@router.get('/cadastro', response_class=HTMLResponse,)
async def root(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request,})

@router.post("/cadastro")
async def postNovo(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    nome: str = Form(""),
    email: str = Form(""),
    senha: str = Form(""),
    confSenha: str = Form(""),
):
    # normalização dos dados
    nome = capitalizar_nome_proprio(nome).strip()
    email = email.lower().strip()
    senha = senha.strip()
    confSenha = confSenha.strip()

    # verificação de erros
    erros = {}
    # validação do campo nome
    is_not_empty(nome, "nome", erros)
    is_person_fullname(nome, "nome", erros)
    # validação do campo email
    is_not_empty(email, "email", erros)
    if is_email(email, "email", erros):
        if ClienteRepo.emailExiste(email):
            add_error("email", "Já existe um Cliente cadastrado com este e-mail.", erros)

    # validação do campo senha
    is_not_empty(senha, "senha", erros)
    is_password(senha, "senha", erros)
    # validação do campo confSenha
    is_not_empty(confSenha, "confSenha", erros)
    is_matching_field_values(confSenha, "confSenha", senha, "Senha", erros)

    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["nome"] = nome
        valores["email"] = email.lower()
        return templates.TemplateResponse(
            "/cadastro.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )

    # inserção no banco de dados
    ClienteRepo.inserir(
        Cliente(
            id=0,
            nome=nome,
            email=email,
            senha=obter_hash_senha(senha)
        )
    )

    # mostra página de sucesso
    return templates.TemplateResponse(
        "/cadastrosucesso.html",
        {"request": request, "usuario": usuario},
    )