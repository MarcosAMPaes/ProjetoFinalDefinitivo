from typing import List
from models.Cliente import Cliente
from models.Cliente import Cliente
from util.Database import Database


class ClienteRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS Usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            token TEXT,
            admin BOOLEAN NOT NULL DEFAULT 0,
            idCliente INTEGER,
            UNIQUE (email),
            CONSTRAINT fkClienteProjeto FOREIGN KEY(idProjeto) REFERENCES projeto(id))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated