import os # for env vars
import discord
from discord.ext import commands

token = os.environ.get('TOKEN')
print('token: {}'.format(token))
bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def greet(ctx):
    await ctx.send("boyyoass")

@bot.group()
async def config(ctx):
    if ctx.user.id == tatanID:
        if ctx.invoked_subcommand is None:
            await ctx.send("no subcommand was called")
        else:
            pass
    else:
        await ctx.send("don\'t fuckin touch my configs")

bot.run(token)