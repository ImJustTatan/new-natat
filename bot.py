import os # for env vars
import discord
from discord.ext import commands

tatanID = 119205994579492864
adminID = 494693989853954048
token = os.environ.get('TOKEN')
print('token: {}'.format(token))
bot = commands.Bot(command_prefix='!')

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
    if ctx.author.id == tatanID:
        if ctx.invoked_subcommand is None:
            await ctx.send("no subcommand was called")
    else:
        await ctx.send("don\'t fuckin touch my configs")

@config.command()
async def play(ctx, *, playing: str):
    await ctx.send('now playing ' + playing)
    gameStat = discord.Game(playing)
    await bot.change_presence(activity=gameStat)
   
@config.command()
async def say(ctx, *, echo: str):
    await ctx.message.delete()
    await ctx.send(echo)

bot.run(token)