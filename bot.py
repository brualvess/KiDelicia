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
    await database.create_tables()
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
async def list_categories(ctx):
    categories = await database.list_category()
    response = f"olá {ctx.author.name}, aqui estão as categorias:\n"
    response += "\n".join([category[0] for category in categories])
    await ctx.send(response)

@bot.command(name="remover_categoria")
async def remove_categories(ctx, category):
    await database.remove_category(category)
    
    await ctx.send(f"categoria {category} removida")

@bot.command(name="inserir_receita")
async def insert_recipe(ctx, name, link, category):
    try:
        response = "mais uma delícia inserida"
        await database.create_recipe(name, link, category)
        await ctx.send(response)
    except IndexError:
        await ctx.send("categoria não encontrada")
    except IntegrityError:
        await ctx.send(f"receita já existe na categoria {category}")
    

@bot.command(name="listar_receitas")
async def list_recipes_category(ctx, category):
    recipes = await database.list_recipes_category(category)
    response = "aqui estão todas as receitas:\n"
    response += "\n".join([recipe[0] for recipe in recipes])
    await ctx.send(response)

@bot.command(name="buscar_receita")
async def get_recipe(ctx, recipe, category):
    recipe_data = await database.get_recipe(recipe, category)
    if len(recipe_data) == 0:
        await ctx.send(f"receita {recipe} não encontrada")
    else:
        response = f"aqui está a receita **{recipe_data[0][0]}**: {recipe_data[0][1]}"
        await ctx.send(response)

@bot.command(name="remover_receita")
async def remove_recipe(ctx, recipe, category):
    await database.remove_recipe(recipe, category)

    await ctx.send(f"receita {recipe} removida")

token = os.getenv("TOKEN")
bot.run(token)