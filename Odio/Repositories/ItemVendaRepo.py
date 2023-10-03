from typing import List
from models.Cliente import Cliente
from util.Database import Database
from models.ItemVenda import ItemVenda


class ItemVendaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS Item_Venda(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idVenda INTEGER,
            idProduto INTEGER,
            quantidade INTEGER NOT NULL,
            subtotal FLOAT,
            FOREIGN KEY (idVenda) REFERENCES venda(id),
            FOREIGN KEY (idProduto) REFERENCES produto(id)
            )
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated
    

    @classmethod
    def inserir(cls, ItemVenda: ItemVenda) -> ItemVenda:
        sql = "INSERT INTO item_venda (idVenda, idProduto, quantidade, subtotal) VALUES (?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (ItemVenda.idVenda, ItemVenda.idProduto, ItemVenda.quantidade, ItemVenda.subtotal)
        )
        if resultado.rowcount > 0:
            ItemVenda.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return ItemVenda
    
    @classmethod
    def obterTodos(cls) -> List[ItemVenda]:
        sql = "SELECT * FROM item_venda"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [ItemVenda(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterItem_VendaPorIdsVenda(cls, id_venda: int) -> List[ItemVenda]:
        sql = "SELECT * FROM item_venda WHERE idVenda = ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id_venda,)).fetchall()
        objetos = [ItemVenda(*x) for x in resultado]
        return objetos
    
    
    @classmethod
    def apagarPorIdVenda(cls, idVenda: int) -> ItemVenda:
        sql = "DELETE FROM item_venda WHERE idVenda=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        cursor.execute(sql, (idVenda,))
        conexao.commit()
        conexao.close()
        return True