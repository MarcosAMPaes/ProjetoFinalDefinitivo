# routes/MainRoutes.py
# routes/MainRoutes.py
import os
from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Repositories.CategoriaRepo import CategoriaRepo
from Repositories.ProdutoRepo import ProdutoRepo
from models.Categoria import Categoria
from models.Produto import Produto
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
    categorias = CategoriaRepo.obterTodos()
    return templates.TemplateResponse("admprodutoadd.html", {"request": request, 'categorias':categorias})

@router.post('/addProduto')
async def root(request: Request, nome: str = Form(...), estoque: int=Form(...), preco: float=Form(...), descricao: str=Form(...), categoria: int=Form(...), imagem: UploadFile=Form(...)):
    nome_arquivo_original = imagem.filename
    nome_raiz, extensao = os.path.splitext(nome_arquivo_original)
    nome_com_extensao = f"{nome_raiz}{extensao}"
    print(nome_com_extensao)
    produto = Produto(id = 0, idCategoria = categoria, nome = nome, descricao=descricao, estoque=estoque, preco=preco, imgProduto=nome_com_extensao)
    ProdutoRepo.inserir(produto)
    return RedirectResponse('/adm',status.HTTP_302_FOUND)

@router.get('/admprodutoalt', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admprodutoalt.html", {"request": request,})

@router.get('/admprodutodel', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("adm_produtodel.html", {"request": request,})

@router.get('/admcategorias', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategorias.html", {"request": request,})

@router.get('/admcategoriaadd', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategoriaadd.html", {"request": request,})

@router.post('/addCategoria')
async def root(nome:str=Form(...)):
    novaCategoria = Categoria(id= 0, nome=nome)
    print(novaCategoria)
    CategoriaRepo.inserir(novaCategoria)
    return RedirectResponse('/adm',status_code=status.HTTP_302_FOUND)


@router.get('/admcategoriasalt', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategoriasalt.html", {"request": request,})

@router.get('/admcategoriasdel', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("admcategoriasdel.html", {"request": request,})