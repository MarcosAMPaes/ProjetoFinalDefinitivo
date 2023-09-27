# routes/MainRoutes.py
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.security import gerar_token, validar_usuario_logado
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/")
async def getIndex(request: Request, logado: bool = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "main/index.html", { "request": request, "logado": logado }

    )
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