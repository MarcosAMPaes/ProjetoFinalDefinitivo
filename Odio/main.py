from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


from Repositories.CategoriaRepo import CategproaRepo
from Repositories.ProdutoRepo import ProdutoRepo


from routes.MainRoutes import router as mainRouter
from routes.ClienteRoutes import router as clienteRouter
from routes.AdminRoutes import router as adminRouter
from routes.CadastroRoutes import router as cadastroRouter
from routes.FechamentoRoutes import router as fechamentoRouter

app = FastAPI()


"""AdministradorRepo.criarTabela()"""
"""CategproaRepo.criarTabela()"""
"""ClienteRepo.criarTabela()"""
"""ItemVenda.criarTabela()"""
"""ProdutoRepo.criarTabela()"""
"""VendaRepo.criarTabela()"""


app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,})

app.include_router(mainRouter)
app.include_router(clienteRouter)
app.include_router(adminRouter)
app.include_router(cadastroRouter)
app.include_router(fechamentoRouter)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)