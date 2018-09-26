import os # for env vars
import discord
from discord.ext import commands

token = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def greet(ctx):
    await ctx.send("boyyoass")

bot.run(token)