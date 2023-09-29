# routes/MainRoutes.py
from fastapi import APIRouter, Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData


router = APIRouter()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/cadastro', response_class=HTMLResponse,)
async def root(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse("cadastro.html", {"request": request,})

@app.get('/carrinho', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("carrinho.html", {"request": request,})

@app.get('/cadastrarnovasenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cadastrarnovasenha.html", {"request": request,})