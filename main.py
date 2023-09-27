from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from Repositorios.ProdutoRepo import ProdutoRepo

app = FastAPI()
ProdutoRepo.criarTabela()


app.mount("/static", StaticFiles(directory="templates/static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,})


@app.get('/cadastro', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request,})

@app.get('/carrinho', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("carrinho.html", {"request": request,})

@app.get('/cadastrarnovasenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cadastrarnovasenha.html", {"request": request,})

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


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)