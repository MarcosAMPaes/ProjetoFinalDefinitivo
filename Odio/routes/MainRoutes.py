# routes/MainRoutes.py
from collections import defaultdict
from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Repositories.ClienteRepo import ClienteRepo
from Repositories.ItemVendaRepo import ItemVendaRepo
from Repositories.ProdutoRepo import ProdutoRepo
from Repositories.CategoriaRepo import CategoriaRepo
from Repositories.VendaRepo import VendaRepo
from models.Cliente import Cliente
from models.ItemVenda import ItemVenda
from models.Venda import Venda
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData
from models.Usuario import Usuario
from util.security import (
    gerar_token,    
    validar_usuario_logado,
    verificar_senha,
)
from util.templateFilters import formatarData
from util.validators import *
import templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")
app = FastAPI()

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/", response_class=HTMLResponse)
async def getIndex(request: Request,pa: int = 1,tp: int = 10):
    produtos = ProdutoRepo.obterTodos()
    categorias = CategoriaRepo.obterTodos()
    filtro = False
    numProdutos = ProdutoRepo.obterPagina(pa, tp)
    totalPaginas = ProdutoRepo.obterQtdePaginas(tp)
    cliente = validar_usuario_logado(request)
    return templates.TemplateResponse("index.html",{ "request": request, "produtos": produtos, "categorias": categorias, 'filtro': filtro ,"numProdutos":numProdutos,
    "totalPaginas": totalPaginas,
    "paginaAtual": pa,
    "tamanhoPagina": tp,
    'cliente': cliente})

@router.get("/base", response_class=HTMLResponse)
async def getIndex(request: Request):
    cliente = validar_usuario_logado(request)
    print(cliente)
    return templates.TemplateResponse("base.html",{ "request": request,'cliente': cliente})

@router.get("/PorCategoria", response_class=HTMLResponse)
async def getIndexCategoria(request: Request, idCategoria: int=Query(...), pa: int = 1,tp: int = 10):
    produtos = ProdutoRepo.obterProdutosCategoria(idCategoria)
    filtro = True
    totalPaginas = ProdutoRepo.obterQtdePaginas(tp)
    return templates.TemplateResponse("index.html", { "request": request, "produtos": produtos, 'filtro': filtro ,"projetos":produtos,
    "totalPaginas": totalPaginas,
    "paginaAtual": pa,
    "tamanhoPagina": tp})

@router.post("/")
async def postProdutoCarrinho(request: Request,
    produto_id: int = Form(...),
    produto_preco: float = Form(...)):
    try:
        token = request.cookies.values().mapping["auth_token"]
        if (token !=""):
            idCliente = ClienteRepo.obterPorToken(token).id
            dataHora = datetime.now()
            novaVenda = Venda(0, idCliente=idCliente, dataHora=dataHora, status=0, valorTotal=produto_preco)
            VendaRepo.inserir(novaVenda)
            novoItemVenda = ItemVenda(id=0, idVenda = novaVenda.id, idProduto=produto_id, quantidade=1, subtotal=produto_preco)
            ItemVendaRepo.inserir(novoItemVenda)
            return RedirectResponse('/carrinho', status_code=status.HTTP_302_FOUND)
        else:
            return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token de autenticação ausente ou inválido. Por favor, faça o login novamente.")




@router.get('/confirmcadastrosenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("confirmcadastrosenha.html", {"request": request,})

@router.get('/confirmcontato', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("confirmcontato.html", {"request": request,})

@router.get('/confirmrecupsenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("confirmrecupsenha.html", {"request": request,})

@router.get('/contato', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request,})

@router.get('/fechamento_endereco', response_class=HTMLResponse)
async def root(request: Request):
    token = request.cookies.values().mapping["auth_token"]
    enderecoCliente = ClienteRepo.obterClientePorToken(token)
    enderecoNumero = ClienteRepo.obterClientePorToken(token)
    return templates.TemplateResponse("fechamento_endereco.html", {"request": request, 'enderecoCliente': enderecoCliente.cep, "enderecoNumero": enderecoNumero.endNumero})

@router.get('/fechamento_itens', response_class=HTMLResponse)
async def root(request: Request):
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
    return templates.TemplateResponse("fechamento_itens.html", {"request": request, 'produtos': produtosUnicos, 'valor': valorTotal})

@router.get('/fechamento_pedido', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("fechamento_pedido.html", {"request": request,})

@router.get('/fechamento_pagamento', response_class=HTMLResponse)
async def root(request: Request):
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
    return templates.TemplateResponse("fechamento_pagamento.html", {"request": request, 'valorTotal':valorTotal})

@router.post('/quitarVendas', response_class=HTMLResponse)
async def root(request: Request):
    print(2)
    token = request.cookies.values().mapping["auth_token"]
    idCliente = ClienteRepo.obterPorToken(token)
    vendasDoCliente = VendaRepo.obterVendaPorCliente(idCliente.id)
    carrinho = []
    for venda in vendasDoCliente:
        carrinho.extend(ItemVendaRepo.obterItem_VendaPorIdsVenda(venda.id))
    for itemVenda in carrinho:
        VendaRepo.quitarVenda(itemVenda.idVenda)
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
        ProdutoRepo.excluirDoEstoque(produto[0].id,produto[1])
    return RedirectResponse('/carrinho', status_code=status.HTTP_302_FOUND)


@router.get('/privacidade', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("privacidade.html", {"request": request,})

@router.get('/produto', response_class=HTMLResponse)
async def root(request: Request, id: int = Query(...)):
    produto = ProdutoRepo.obterProdutosPorId(id)
    return templates.TemplateResponse("produto.html", {"request": request, 'produto': produto[0]})

@router.get('/quemsomos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("quemsomos.html", {"request": request,})

@router.get('/recuperarsenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("recuperarsenha.html", {"request": request,})

@router.get('/termos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("termos.html", {"request": request,})

@router.get('/trocas', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("trocas.html", {"request": request,})



@router.get("/")
async def getIndex(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    categoria = CategoriaRepo.obterTodos()
    for categoria in categoria:
        categoria.integrantes = CategoriaRepo.obterProdutos(categoria.id)
    return templates.TemplateResponse(
        "index.html", {"request": request, "usuario": usuario, "categoria": categoria}
    )


@router.get("/login")
async def getLogin(
    request: Request, cliente: Cliente = Depends(validar_usuario_logado)
):
    return templates.TemplateResponse(
        "login.html", {"request": request, "cliente": cliente}
    )


@router.post("/login")
async def postLogin(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    email: str = Form(""),
    senha: str = Form(""),
    returnUrl: str = Query("/"),
):
    # normalização de dados
    email = email.strip().lower()
    senha = senha.strip()
    
    # validação de dados
    erros = {}
    # validação do campo email
    is_not_empty(email, "email", erros)
    is_email(email, "email", erros)
    # validação do campo senha
    is_not_empty(senha, "senha", erros)
        
    # só checa a senha no BD se os dados forem válidos
    hash_senha_bd = ClienteRepo.obterSenhaDeEmail(email)
    if hash_senha_bd:
        print(senha)
        print(verificar_senha(senha, hash_senha_bd))
        if verificar_senha(senha, hash_senha_bd):
            token = gerar_token()
            if ClienteRepo.alterarToken(email, token):
                response = RedirectResponse('/', status.HTTP_302_FOUND)
                response.set_cookie(
                    key="auth_token", value=token, max_age=1800, httponly=True
                )
                return response
            else:
                raise Exception(
                    "Não foi possível alterar o token do usuário no banco de dados."
                )
        else:            
            add_error("senha", "Senha não confere.", erros)
    else:
        add_error("email", "Usuário não cadastrado.", erros)

    # se tem algum erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["email"] = email        
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )

@router.get("/logout")
async def getLogout( request: Request, usuario: Usuario = Depends(validar_usuario_logado)):   
    if (usuario):
        ClienteRepo.alterarToken(usuario.email, "") 
    response = RedirectResponse("/", status.HTTP_302_FOUND)
    response.set_cookie(key="auth_token", value="", httponly=True, expires="1970-01-01T00:00:00Z")   
    return response