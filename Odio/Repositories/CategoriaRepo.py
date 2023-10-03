# repositories/ProjetoRepo.py
from typing import List
from models.Categoria import Categoria
from util.Database import Database

class CategoriaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL)
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, categoria: Categoria) -> Categoria:        
        sql = "INSERT INTO categoria (nome) VALUES (?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (categoria.nome))
        if (resultado.rowcount > 0):            
            categoria.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return categoria
    
    @classmethod
    def alterar(cls, categoria: Categoria) -> Categoria:
        sql = "UPDATE categoria SET nome=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (categoria.nome, categoria.id))
        if (resultado.rowcount > 0):            
            conexao.commit()
            conexao.close()
            return categoria
        else: 
            conexao.close()
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM categoria WHERE id=?"
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
    def obterTodos(cls) -> List[Categoria]:
        sql = "SELECT id, nome FROM categoria ORDER BY nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Categoria(*x) for x in resultado]
        return objetos
    
    
    @classmethod
    def obterPorId(cls, id: int) -> Categoria:
        sql = "SELECT id, nome FROM projeto WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        objeto = Categoria(*resultado)
        return objeto
    