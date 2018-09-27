import os # for env vars
import discord
from discord.ext import commands
from random import choice

tatanID = 119205994579492864
adminID = 494693989853954048
token = os.environ.get('TOKEN')
print('token: {}'.format(token))
bot = commands.Bot(command_prefix='!')
fyou = {'fuck off', 'fuck you',
        'stop it', 'im gonna kill you'}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.event()
async def on_message(msg):
    if ':v' in msg.content:
        await msg.channel.send(':gun:')
        await msg.author.send(choice(fyou))
    
    await bot.process_commands(message)

@bot.command()
async def greet(ctx):
    """Greets you."""
    await ctx.send("boyyoass")
    
@bot.group()
async def config(ctx):
    """Configuration commands. Only <@>1 can access them19205994579492864."""
    if ctx.author.id == tatanID:
        if ctx.invoked_subcommand is None:
            await ctx.send("no subcommand was called")
    else:
        await ctx.send("don\'t fuckin touch my configs")
        pass

@config.command()
async def play(ctx, *, playing: str):
    await ctx.send('now playing ' + playing.lower())
    gameStat = discord.Game(playing)
    await bot.change_presence(activity=gameStat)

@config.command()
async def stream(ctx, *, streaming: str):
    await ctx.send('now streaming ' + streaming.lower())
    streamStat = discord.Streaming(streaming)
    await bot.change_presence(activity=streamStat)

@config.command()
async def say(ctx, *, echo: str):
    await ctx.message.delete()
    await ctx.send(echo)

bot.run(token)