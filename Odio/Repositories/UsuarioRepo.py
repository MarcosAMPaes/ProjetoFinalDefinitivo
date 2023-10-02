from typing import List
from util.Database import Database
from models.Usuario import Usuario

class UsuarioRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idCliente INT NOT NULL,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            admin BOOLEAN NOT NULL DEFAULT 0,
            UNIQUE (email),
            FOREIGN KEY(idCliente) REFERENCES cliente(id))
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated