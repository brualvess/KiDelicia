from sqlite3 import IntegrityError
import discord
from discord.ext import  commands, tasks
from database import Database
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

database = Database()

@bot.event
async def on_ready():
    database.create_table_category()
    print(f"Tudo ok! Estou conectado como {bot.user}")

@bot.command(name="ping")
async def ping(ctx):
    response = "pong"

    await ctx.send(response)

@bot.command(name="inserir_categoria")
async def insert_category(ctx, category):
    try:
        response = "categoria inserida"
        await database.create_category(category)
        await ctx.send(response)
    except IntegrityError:
        await ctx.send("categoria já existe!")

@bot.command(name="listar_categorias")
async def get_categories(ctx):
    categories = await database.get_category()
    response = f"olá {ctx.author.name}, aqui estão as categorias:\n"
    response += "\n".join([category[0] for category in categories])
    await ctx.send(response)

@bot.command(name="remover_categoria")
async def get_categories(ctx, category):
    await database.remove_category(category)
    
    await ctx.send(f"categoria {category} removida")

token = os.getenv("TOKEN")
bot.run(token)