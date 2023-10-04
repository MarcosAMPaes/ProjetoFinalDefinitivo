# routes/MainRoutes.py
# routes/MainRoutes.py
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get('/adm', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("adm.html", {"request": request,})

@router.get('/admprodutos', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admprodutos.html", {"request": request,})

@router.get('/admprodutoadd', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admprodutoadd.html", {"request": request,})

@router.get('/admprodutoalt', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admprodutoalt.html", {"request": request,})

@router.get('/admprodutodel', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("adm_produtodel.html", {"request": request,})

@router.get('/admcategorias', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategorias.html", {"request": request,})

@router.get('/admcategoriasadd', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategoriasadd.html", {"request": request,})

@router.get('/admcategoriasalt', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategoriasalt.html", {"request": request,})

@router.get('/admcategoriasdel', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategoriasdel.html", {"request": request,})