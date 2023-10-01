# routes/MainRoutes.py
from fastapi import APIRouter, Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Repositories.ItemVendaRepo import ItemVendaRepo
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData


router = APIRouter()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@router.get('/cadastro', response_class=HTMLResponse,)
async def root(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request,})

@router.get('/carrinho', response_class=HTMLResponse)
async def root(request: Request):
    carrinho = ItemVendaRepo.obterTodos()
    return templates.TemplateResponse("carrinho.html", {"request": request, 'carrinho': carrinho})

@router.get('/cadastrarnovasenha', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cadastrarnovasenha.html", {"request": request,})