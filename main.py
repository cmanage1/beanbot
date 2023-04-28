import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv
import openai

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_ai_answer(msg: str):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "user", "content": msg},
    ])
    return completion.choices[0].message.content

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def hello(ctx):
    await ctx.send("Bean bot says hello")

@bot.command()
async def add(ctx, left="", right=""):
    """Adds two numbers together."""
    try:
        await ctx.send(int(left) + int(right))
    except:
        await ctx.send("Invalid, should be format '!add 2 3'")

@commands.command(name='ask', aliases=['!'], brief='Ask GPT3.5 Turbo')
async def special_command(ctx, *args):
    if args:
        msg = " ".join(args)
        logging.info(msg)
        res = get_ai_answer(msg) #OpenAI API call
        await ctx.send(res)
    else:
        await ctx.send("Ask me anything! Ex: '!! who invented discord?' ")

load_dotenv()
bot.add_command(special_command)
dt=os.getenv('DISCORD_TOKEN')
logging.basicConfig(level=logging.DEBUG)
bot.run(dt)
