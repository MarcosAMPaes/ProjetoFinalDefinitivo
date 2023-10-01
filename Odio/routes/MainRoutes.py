# routes/MainRoutes.py
from datetime import datetime
from fastapi import APIRouter, Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Repositories.ClienteRepo import ClienteRepo
from Repositories.ItemVendaRepo import ItemVendaRepo
from Repositories.ProdutoRepo import ProdutoRepo
from Repositories.VendaRepo import VendaRepo
from models.ItemVenda import ItemVenda
from models.Venda import Venda
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData
import templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")
app = FastAPI()

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/", response_class=HTMLResponse)
async def getIndex(request: Request):
    produtos = ProdutoRepo.obterTodos()
    return templates.TemplateResponse("index.html", { "request": request, "produtos": produtos })

@router.post("/")
async def postProdutoCarrinho(request: Request,
    produto_id: int = Form(...),
    produto_preco: float = Form(...)):
    
    status = 0
    token = gerar_token()
    ClienteRepo.inserirToken(token)
    idCliente = ClienteRepo.obterPorToken(token).id
    dataHora = datetime.now()
    novaVenda = Venda(id=0, idCliente=idCliente, dataHora=dataHora, status=status, valorTotal=produto_preco)
    VendaRepo.inserir(novaVenda)
    novoItemVenda = ItemVenda(id=0, idVenda = novaVenda.id, idProduto=produto_id, quantidade=1, subtotal=produto_preco)
    ItemVendaRepo.inserir(novoItemVenda)
    response = RedirectResponse('/carrinho', status_code=302)
    response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
    return response



@router.get('/cliente_contatos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_contatos.html", {"request": request,})

@router.get('/cliente_dados', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_dados.html", {"request": request,})

@router.get('/cliente_endereco', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_endereco.html", {"request": request,})

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
async def root(request: Request):
    return templates.TemplateResponse("cliente.html", {"request": request,})

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
    return templates.TemplateResponse("fechamento_endereco.html", {"request": request,})

@router.get('/fechamento_itens', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("fechamento_itens.html", {"request": request,})

@router.get('/fechamento_pedido', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("fechamento_pedido.html", {"request": request,})

@router.get('/fechamento_pagamento', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("fechamento_pagamento.html", {"request": request,})

@router.get('/login', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,})

@router.get('/privacidade', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("privacidade.html", {"request": request,})

@router.get('/produto', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("produto.html", {"request": request,})

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



@router.get("/login")
async def getLogin(request: Request, logado: bool = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "main/login.html", { "request": request, "logado": logado }
    )

@router.post("/login")
async def postLogin(
    email: str = Form(...),
    senha: str = Form(...)):
    if email == "usuario@email.com" and senha == "123456":
        token = gerar_token()
        response = RedirectResponse("/", status.HTTP_302_FOUND)
        response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
        return response
    else:
        return RedirectResponse("/login", status.HTTP_302_FOUND)
    
@router.get("/logout")
async def getLogout(request: Request):
    response = RedirectResponse("/", status.HTTP_302_FOUND)
    response.set_cookie(key="auth_token", value="", httponly=True, 
                        expires="1970-01-01T00:00:00Z")
    return response