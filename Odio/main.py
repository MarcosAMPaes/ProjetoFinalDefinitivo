from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from Repositories.AdministradorRepo import AdministradorRepo


from Repositories.CategoriaRepo import CategoriaRepo
from Repositories.ClienteRepo import ClienteRepo
from Repositories.ItemVendaRepo import ItemVendaRepo
from Repositories.ProdutoRepo import ProdutoRepo
from Repositories.UsuarioRepo import UsuarioRepo
from Repositories.VendaRepo import VendaRepo


from routes.MainRoutes import router as mainRouter
from routes.ClienteRoutes import router as clienteRouter
from routes.AdminRoutes import router as adminRouter
from routes.CadastroRoutes import router as cadastroRouter
from routes.FechamentoRoutes import router as fechamentoRouter

CategoriaRepo.criarTabela()
ProdutoRepo.criarTabela()
ClienteRepo.criarTabela()
AdministradorRepo.criarTabela()
VendaRepo.criarTabela()
ItemVendaRepo.criarTabela()
UsuarioRepo.criarTabela()

app = FastAPI()





app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(mainRouter)
app.include_router(clienteRouter)
app.include_router(adminRouter)
app.include_router(cadastroRouter)
app.include_router(fechamentoRouter)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
    