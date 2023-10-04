from typing import List
from models.Cliente import Cliente
from util.Database import Database

class ClienteRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS cliente(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endNumero TEXT,
            cep TEXT,
            token TEXT,
            admin BOOLEAN NOT NULL DEFAULT 0,
            UNIQUE (email))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated

   

    @classmethod
    def inserir(cls, cliente: Cliente) -> Cliente:
        sql = "INSERT INTO cliente (nome, email, senha, telefone, endNumero, cep, token) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (cliente.nome, cliente.email, cliente.senha, cliente.telefone, cliente.endNumero, cliente.cep, cliente.token)
        )
        if resultado.rowcount > 0:
            cliente.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return cliente

    @classmethod
    def alterar(cls, cliente: Cliente) -> Cliente:
        sql = "UPDATE cliente SET nome=?, cliente.email=?, telefone=?, endNumero=?, cep=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (cliente.nome, cliente.email, cliente.telefone,cliente.endNumero, cliente.cep, cliente.id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return cliente
        else:
            conexao.close()
            return None

    @classmethod
    def alterarSenha(cls, id: int, senha: str) -> bool:
        sql = "UPDATE cliente SET senha=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (senha, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def inserirToken(cls, token: str) -> bool:
        sql = "UPDATE cliente SET token=? WHERE id=1"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def alterarAdmin(cls, id: int, admin: bool) -> bool:
        sql = "UPDATE cliente SET admin=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (admin, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def aprovarCadastro(cls, id: int, aprovar: bool = True) -> bool:
        sql = "UPDATE cliente SET aprovado=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (aprovar, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def emailExiste(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM cliente WHERE email=?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()        
        return bool(resultado[0])

    @classmethod
    def obterSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT senha FROM cliente WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM cliente WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def obterTodos(cls) -> List[Cliente]:
        sql = "SELECT cliente.id, cliente.nome, cliente.email, cliente.admin, cliente.idProjeto, projeto.nome AS nomeProjeto FROM cliente INNER JOIN projeto ON cliente.idProjeto = projeto.id ORDER BY cliente.nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Cliente(
                id=x[0],
                nome=x[1],
                email=x[2],
                admin=x[3],
                idProjeto=x[4],
                nomeProjeto=x[5],
            )
            for x in resultado
        ]
        return objetos

    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Cliente]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT cliente.id, cliente.nome, cliente.email, cliente.admin, cliente.idProjeto, projeto.nome AS nomeProjeto FROM cliente INNER JOIN projeto ON cliente.idProjeto = projeto.id WHERE cliente.aprovado = 1 ORDER BY cliente.nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Cliente(
                id=x[0],
                nome=x[1],
                email=x[2],
                admin=x[3],
                idProjeto=x[4],
                nomeProjeto=x[5],
            )
            for x in resultado
        ]
        return objetos

    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM cliente WHERE aprovado = 1 AND idProjeto IS NOT NULL) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina,)).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPaginaAprovar(cls, pagina: int, tamanhoPagina: int) -> List[Cliente]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT cliente.id, cliente.nome, cliente.email, cliente.admin, cliente.idProjeto, projeto.nome AS nomeProjeto FROM cliente INNER JOIN projeto ON cliente.idProjeto = projeto.id WHERE cliente.aprovado = 0 ORDER BY cliente.dataCadastro LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Cliente(
                id=x[0],
                nome=x[1],
                email=x[2],
                admin=x[3],
                idProjeto=x[4],
                nomeProjeto=x[5],
            )
            for x in resultado
        ]
        return objetos

    @classmethod
    def obterQtdePaginasAprovar(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM cliente WHERE aprovado = 0 AND idProjeto IS NOT NULL) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina,)).fetchone()
        return int(resultado[0])

    @classmethod
    def obterQtdeAprovar(cls) -> int:
        sql = "SELECT COUNT(*) FROM cliente WHERE aprovado = 0 AND idProjeto IS NOT NULL"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPorId(cls, id: int) -> Cliente | None:
        sql = "SELECT cliente.id, cliente.nome, cliente.email, cliente.admin, cliente.aprovado, cliente.idProjeto, projeto.nome AS nomeProjeto FROM cliente INNER JOIN projeto ON cliente.idProjeto = projeto.id WHERE cliente.id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()
        if (resultado):
            objeto = Cliente(
                id=resultado[0],
                nome=resultado[1],
                email=resultado[2],
                admin=resultado[3],
                aprovado=resultado[4],
                idProjeto=resultado[5],
                nomeProjeto=resultado[6],
            )
            return objeto
        else: 
            return None
        

    @classmethod
    def obterPorToken(cls, token: str) -> Cliente:
        sql = "SELECT * FROM cliente WHERE token=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token,)).fetchone()
        objeto = Cliente(*resultado) if resultado else None
        return objeto
    @classmethod
    def obterIntegrantes(cls, id: int) -> List[str]:
        sql = "SELECT nome FROM produto WHERE idCategoria=? and aprovado=1 ORDER BY nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchall()
        if resultado:
            return [x[0] for x in resultado]
        else:
            return []
        
    @classmethod
    def alterarToken(cls, email: str, token: str) -> bool:
        sql = "UPDATE cliente SET token=? WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, email))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
    @classmethod
    def alterarAdmin(cls, id: int, admin: bool) -> bool:
        sql = "UPDATE cliente SET admin=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (admin, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def emailExiste(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM cliente WHERE email=?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()        
        return bool(resultado[0])
    
    @classmethod
    def obterClientePorToken(cls, token: str) -> Cliente:
        sql = "SELECT id, nome, email, senha, telefone, endNumero, cep, token, admin FROM cliente WHERE token=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Cliente(*resultado)
            return objeto
        else:
            return None
        

    @classmethod
    def inserirPorToken(cls, token: str, cep: str, endNumero: str) -> Cliente:
        sql = "UPDATE cliente SET cep=?, endNumero=? WHERE token=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (cep, endNumero, token))
        conexao.commit()
        conexao.close()
        return resultado.rowcount > 0
