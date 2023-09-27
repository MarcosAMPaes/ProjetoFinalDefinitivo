# routes/MainRoutes.py
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")