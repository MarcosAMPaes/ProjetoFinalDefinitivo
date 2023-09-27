# repositories/ProjetoRepo.py
from typing import List
from models.Administrador import Administrador
from util.Database import Database

class AdministradorRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS administrador (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idUsuario INTEGER,
            nome TEXT NOT NULL,
            email INT NOT NULL,
            telefone TEXT NOT NULL,
            FOREIGN KEY (idUsuario) REFERENCES usuario(id))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, administrador: Administrador) -> Administrador:        
        sql = "INSERT INTO administrador (idUsuario, nome, email, telefone) VALUES (?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (administrador.idUsuario, administrador.nome, administrador.estoque, administrador.preco, administrador.descricao))
        if (resultado.rowcount > 0):            
            administrador.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return administrador
    
    @classmethod
    def alterar(cls, administrador: Administrador) -> Administrador:
        sql = "UPDATE administrador SET idUsuario=?, nome=?, email=?, telefone=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (administrador.nome, administrador.estoque, administrador.preco, administrador.descricao, administrador.id))
        if (resultado.rowcount > 0):            
            conexao.commit()
            conexao.close()
            return administrador
        else: 
            conexao.close()
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM administrador WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, ))
        if (resultado.rowcount > 0):
            conexao.commit()
            conexao.close()
            return True
        else: 
            conexao.close()
            return False
        
    @classmethod
    def obterTodos(cls) -> List[Administrador]:
        sql = "SELECT idUsuario, nome, email, telefone FROM administrador ORDER BY nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Administrador(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Administrador]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT idUsuario, nome, email, telefone FROM administrador ORDER BY nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [Administrador(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM administrador) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])
    
    @classmethod
    def obterPorId(cls, id: int) -> Administrador:
        sql = "SELECT idUsuario, nome, email, telefone FROM projeto WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        objeto = Administrador(*resultado)
        return objeto