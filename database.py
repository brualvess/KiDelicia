import sqlite3
class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("receitas.db")
        self.enable_foreign_keys()
        
    def enable_foreign_keys(self):
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

    async def get_categoryId(self, category):
        cursor = self.connection.cursor()
        get_categoryId = "SELECT id FROM categorias WHERE nome = ?"
        cursor.execute(get_categoryId, (category,))
        id = cursor.fetchall()
        id = id[0][0]
        cursor.close()
        return id


    async def _create_table_category(self) -> None:
        cursor = self.connection.cursor()
        table = """ CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY,
                    nome VARCHAR(256) NOT NULL,
                    UNIQUE(nome)
                )"""
        cursor.execute(table)
        self.connection.commit()
        cursor.close()

    async def _create_table_recipe(self) -> None:
        cursor = self.connection.cursor()
        table = """ CREATE TABLE IF NOT EXISTS receitas (
                    id INTEGER PRIMARY KEY,
                    nome VARCHAR(256) NOT NULL,
                    link VATCHAR(256) NOT NULL,
                    categoria_id INTEGER NOT NULL,
                    FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE CASCADE,
                    UNIQUE(nome, categoria_id)
                )"""
        cursor.execute(table)
        self.connection.commit()
        cursor.close()
    
    async def create_tables(self) -> None:
        await self._create_table_category()
        await self._create_table_recipe()

    async def create_category(self, category) -> None:
        cursor = self.connection.cursor()
        insert_category = """  INSERT INTO categorias (nome)
                        VALUES (?)
                 """
        cursor.execute(insert_category, (category,))
        self.connection.commit()
        cursor.close()
    
    async def list_category(self) -> list:
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

    async def create_recipe(self, name, link, category) -> None:
        cursor = self.connection.cursor()
        insert_recipe = """ INSERT INTO receitas (nome, link, categoria_id)
                        VALUES (?,?,?)
                    """
        categoryId = await self.get_categoryId(category)
        cursor.execute(insert_recipe, (name, link, categoryId))
        self.connection.commit()
        cursor.close() 

    async def list_recipes_category(self, category) -> list:
        cursor = self.connection.cursor()
        id = await self.get_categoryId(category)
        get = "SELECT nome FROM receitas WHERE categoria_id = ?"
        cursor.execute(get, (id,))
        recipes = cursor.fetchall()
        cursor.close()
        
        return recipes

    async def get_recipe(self, recipe, category) -> list:
        cursor = self.connection.cursor()
        categoryId = await self.get_categoryId(category)
        query_recipe = """SELECT nome, link FROM  receitas WHERE nome = ? AND categoria_id = ?"""
        cursor.execute(query_recipe, (recipe, categoryId,))
        result = cursor.fetchall()
        cursor.close()

        return result 

    async def remove_recipe(self, recipe, category):
        cursor = self.connection.cursor()
        categoryId = await self.get_categoryId(category)
        remove = "DELETE FROM receitas WHERE nome = ? and categoria_id = ?"
        cursor.execute(remove, (recipe, categoryId,))
        self.connection.commit()
        cursor.close()
