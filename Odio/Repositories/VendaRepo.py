from typing import List
from models.Venda import Venda
from util.Database import Database


class VendaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS venda(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idCliente INTEGER NOT NULL,
            dataHora DATETIME NOT NULL,
            status BOOLEAN NOT NULL DEFAULT 0,
            valorTotal REAL NOT NULL,
            FOREIGN KEY (idCliente) REFERENCES cliente(id))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conexao.commit()
        conexao.close()
        return tableCreated
    

    @classmethod
    def inserir(cls, venda: Venda) -> Venda:
        sql = "INSERT INTO venda (idCliente, dataHora, status, valorTotal) VALUES (?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (venda.idCliente, venda.dataHora, venda.status, venda.valorTotal)
        )
        if resultado.rowcount > 0:
            venda.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return Venda
    
    @classmethod
    def obterVendaPorCliente(cls, idCliente: int) -> Venda:
        sql = "SELECT * FROM venda WHERE idCliente = ? and status=0"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql,(idCliente,)).fetchall()
        objetos = [Venda(*x) for x in resultado]
        return objetos
    
    @classmethod
    def excluirUmaVenda(cls, idVenda: int) -> Venda:
        sql = "DELETE FROM venda WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        cursor.execute(sql, (idVenda,))
        conexao.commit()
        conexao.close()
        return True
    
    @classmethod
    def quitarVenda(cls,id:int) -> Venda:
        sql = "UPDATE venda SET status=1 WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,))
        conexao.commit()
        conexao.close()
        return resultado.rowcount > 0
