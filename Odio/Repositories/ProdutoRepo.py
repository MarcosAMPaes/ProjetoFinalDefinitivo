# repositories/produtoRepo.py
from typing import List
from models.Produto import Produto
from util.Database import Database

class ProdutoRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idCategoria INT NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            estoque INT NOT NULL,
            preco FLOAT NOT NULL,
            imgProduto TEXT,
            FOREIGN KEY (idCategoria) REFERENCES categoria(id))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, produto: Produto) -> Produto:        
        sql = "INSERT INTO produto (idCategoria, nome, descricao, estoque, preco, imgProduto) VALUES (?, ?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (produto.idCategoria, produto.nome, produto.descricao, produto.estoque, produto.preco, produto.imgProduto))
        if (resultado.rowcount > 0):            
            produto.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return produto
    
    @classmethod
    def alterar(cls, produto: Produto) -> Produto:
        sql = "UPDATE produto SET nome=?, estoque=?, preco=?, descricao=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (produto.nome, produto.estoque, produto.preco, produto.descricao, produto.id))
        if (resultado.rowcount > 0):            
            conexao.commit()
            conexao.close()
            return produto
        else: 
            conexao.close()
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM produto WHERE id=?"
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
    def obterTodos(cls) -> List[Produto]:
        sql = "SELECT id, idCategoria, nome, descricao, estoque, preco, imgProduto FROM produto WHERE estoque != 0 ORDER BY nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Produto(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Produto]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT id, idCategoria, nome, descricao, estoque, preco, imgProduto FROM produto ORDER BY nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [Produto(*x) for x in resultado]
        return objetos

    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM produto) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])
    
    @classmethod
    def obterProdutosPorId(cls, id: int) -> List[Produto]:
        sql = "SELECT id, idCategoria, nome, descricao, estoque, preco, imgProduto FROM produto WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchall()
        objetos = [Produto(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterProdutosCategoria(cls, idCategoria: int) -> List[Produto]:
        sql = "SELECT id, idCategoria, nome, descricao, estoque, preco, imgProduto FROM produto WHERE idCategoria=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idCategoria,)).fetchall()
        objetos = [Produto(*x) for x in resultado]
        return objetos
    

    @classmethod
    def excluirDoEstoque(cls, id: int, contagem:int) -> Produto:
        sql = "UPDATE produto SET estoque = estoque - ? WHERE id = ?;"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        cursor.execute(sql, (contagem, id))
        conexao.commit()
        conexao.close()
        return True