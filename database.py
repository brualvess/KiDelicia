import sqlite3
class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("receitas.db")
        
    def create_table_category(self) -> None:
        cursor = self.connection.cursor()
        table = """ CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY,
                    nome VARCHAR(256) NOT NULL,
                    UNIQUE(nome)
                )"""
        cursor.execute(table)
        self.connection.commit()
        cursor.close()
    
    async def create_category(self, category) -> None:
        cursor = self.connection.cursor()
        insert_category = """  INSERT INTO categorias (nome)
                        VALUES (?)
                 """
        cursor.execute(insert_category, (category,))
        self.connection.commit()
        cursor.close()
    
    async def get_category(self) -> list:
        cursor = self.connection.cursor()
        get = "SELECT nome FROM categorias"
        cursor.execute(get)
        categories = cursor.fetchall()
        cursor.close()
        
        return categories
        
    async def remove_category(self, category) -> None:
        cursor = self.connection.cursor()
        remove = "DELETE FROM categorias WHERE nome = ?"
        cursor.execute(remove, (category,))
        self.connection.commit()
        cursor.close()