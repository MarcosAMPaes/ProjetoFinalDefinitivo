from datetime import datetime
from Repositories.ItemVendaRepo import ItemVendaRepo
from Repositories.ProdutoRepo import ProdutoRepo
from Repositories.VendaRepo import VendaRepo
from models.ItemVenda import ItemVenda
from models.Venda import Venda
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData
# routes/ProjetoRoutes.py
from fastapi import APIRouter, Depends, Form, Path, HTTPException, Query, Request, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from util.security import obter_hash_senha, validar_usuario_logado, verificar_senha
from util.templateFilters import capitalizar_nome_proprio, formatarData
from Repositories.ClienteRepo import ClienteRepo
from Repositories.ItemVendaRepo import ItemVendaRepo
from util.validators import *
from models.Cliente import Cliente
from models.Usuario import Usuario

from collections import defaultdict


router = APIRouter()

app = FastAPI()

templates = Jinja2Templates(directory="templates")



@router.get('/carrinho', response_class=HTMLResponse)
async def root(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        if usuario.admin:
            return RedirectResponse('/adm',status_code=status.HTTP_302_FOUND)
        else:
            token = request.cookies.values().mapping["auth_token"]
            idCliente = ClienteRepo.obterPorToken(token)
            vendasDoCliente = VendaRepo.obterVendaPorCliente(idCliente.id)
            carrinho = []
            for venda in vendasDoCliente:
                carrinho.extend(ItemVendaRepo.obterItem_VendaPorIdsVenda(venda.id))
            produtos = []
            for item_venda in carrinho:
                produtos.extend(ProdutoRepo.obterProdutosPorId(item_venda.idProduto))
            contagem_produtos = defaultdict(int)
            for produto in produtos:
                contagem_produtos[produto.id] += 1
            produtosUnicos = []
            valorTotal = 0
            for produto in produtos:
                if contagem_produtos[produto.id] > 0:
                    produtosUnicos.append((produto, contagem_produtos[produto.id]))
                    contagem_produtos[produto.id] = 0
            for produto in produtosUnicos:
                valorTotal += produto[0].preco*produto[1]
            return templates.TemplateResponse("carrinho.html", {"request": request, 'produtos': produtosUnicos, 'valor': valorTotal})
    else:
        return RedirectResponse('/login',status_code=status.HTTP_302_FOUND)


@router.post('/itemMais1')
async def postItemMais1(request: Request, idProduto: int=Query(...)):
    token = request.cookies.values().mapping["auth_token"]
    idCliente = ClienteRepo.obterPorToken(token).id
    dataHora = datetime.now()
    produto = ProdutoRepo.obterProdutosPorId(idProduto)
    novaVenda = Venda(0, idCliente=idCliente, dataHora=dataHora, status=0, valorTotal=produto[0].preco)
    VendaRepo.inserir(novaVenda)
    novoItemVenda = ItemVenda(id=0, idVenda = novaVenda.id, idProduto=idProduto, quantidade=1, subtotal=produto[0].preco)
    ItemVendaRepo.inserir(novoItemVenda)
    print(idProduto)
    return RedirectResponse('/carrinho',status_code=status.HTTP_302_FOUND)

@router.post('/itemMenos1')
async def postItemMenos1(request: Request):
    token = request.cookies.values().mapping["auth_token"]
    idCliente = ClienteRepo.obterPorToken(token).id
    vendasDoCliente = VendaRepo.obterVendaPorCliente(idCliente)
    ItemVendaRepo.apagarPorIdVenda(vendasDoCliente[-1].id)
    VendaRepo.excluirUmaVenda(vendasDoCliente[-1].id)
    return RedirectResponse('/carrinho',status_code=status.HTTP_302_FOUND)


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
    telefone: str = Form("")
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

    # inserção no banco de dados
    ClienteRepo.inserir(
        Cliente(
            id=0,
            nome=nome,
            email=email,
            senha=obter_hash_senha(senha),
            telefone = telefone
        )
    )

    # mostra página de sucesso
    token = gerar_token()
    ClienteRepo.inserirToken(token)
    response = RedirectResponse("/cadastrosucesso", status.HTTP_302_FOUND)
    response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
    return response


@router.get('/cadastrosucesso', response_class=HTMLResponse,)
async def root(request: Request):
    return templates.TemplateResponse("cadastrosucesso.html", {"request": request,})

@router.get('/cliente_contatos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_contatos.html", {"request": request,})

@router.get('/cliente_dados', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_dados.html", {"request": request,})

@router.get('/cliente_endereco', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_endereco.html", {"request": request,})

@router.post('/cliente_endereco')
async def root(request: Request, cep: str=Form(...), numero: str=Form(...)):
    token = request.cookies.values().mapping["auth_token"]
    ClienteRepo.inserirPorToken(token, cep, numero)
    return RedirectResponse('/fechamento_endereco',status_code=status.HTTP_302_FOUND)


@router.get('/cliente_favoritos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_favoritos.html", {"request": request,})

@router.get('/cliente_pedidos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_pedidos.html", {"request": request,})

@router.get('/cliente_senha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_senha.html", {"request": request,})

@router.get('/cliente', response_class=HTMLResponse)
async def getCliente(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
     if usuario:
        if usuario.admin:
            return RedirectResponse('/adm',status_code=status.HTTP_302_FOUND)
        else:  
            return templates.TemplateResponse("cliente.html", {"request": request,})
     else:
         return RedirectResponse('/login',status_code=status.HTTP_302_FOUND)