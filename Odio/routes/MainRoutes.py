# routes/MainRoutes.py
from fastapi import APIRouter, Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData


router = APIRouter()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/")
async def getIndex(request: Request, logado: bool = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "main/index.html", { "request": request, "logado": logado }

    )

@app.get('/cliente_contatos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_contatos.html", {"request": request,})

@app.get('/cliente_dados', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_dados.html", {"request": request,})

@app.get('/cliente_endereco', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_endereco.html", {"request": request,})

@app.get('/cliente_favoritos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_favoritos.html", {"request": request,})

@app.get('/cliente_pedidos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_pedidos.html", {"request": request,})

@app.get('/cliente_senha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente_senha.html", {"request": request,})

@app.get('/cliente', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cliente.html", {"request": request,})

@app.get('/confirmcadastrosenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("confirmcadastrosenha.html", {"request": request,})

@app.get('/confirmcontato', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("confirmcontato.html", {"request": request,})

@app.get('/confirmrecupsenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("confirmrecupsenha.html", {"request": request,})

@app.get('/contato', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request,})

@app.get('/fechamento_endereco', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("fechamento_endereco.html", {"request": request,})

@app.get('/fechamento_itens', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("fechamento_itens.html", {"request": request,})

@app.get('/fechamento_pedido', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("fechamento_pedido.html", {"request": request,})

@app.get('/fechamento_pagamento', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("fechamento_pagamento.html", {"request": request,})

@app.get('/login', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,})

@app.get('/privacidade', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("privacidade.html", {"request": request,})

@app.get('/produto', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("produto.html", {"request": request,})

@app.get('/quemsomos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("quemsomos.html", {"request": request,})

@app.get('/recuperarsenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("recuperarsenha.html", {"request": request,})

@app.get('/termos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("termos.html", {"request": request,})

@app.get('/trocas', response_class=HTMLResponse)
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