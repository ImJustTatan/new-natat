import os # for env vars
import discord
from discord.ext import commands
from random import choice

tatanID = 119205994579492864
adminID = 494693989853954048
guildID = 290144092841836556

token = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix='!', owner_id=tatanID, description='tatan\'s bot.')

fyou = ['fuck off', 'fuck you',
		'stop it', 'im gonna kill you']
print(fyou)

def docstring_parameter(*sub):
	"""useful function for using variables in docstrings
	i.e. @docstring_parameter(fyou)"""
	def dec(obj):
		obj.__doc__ = obj.__doc__.format(*sub)
		return obj
	return dec

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	
@bot.event
async def on_message(msg):
	if ':v' in msg.content:
		await msg.channel.send(':gun:')
		await msg.author.send(choice(fyou))
	
	await bot.process_commands(msg)

greet_aliases = ['hello', 'salute', 'test']
@bot.command(description='A simple command for testing the bot.', aliases=greet_aliases)
async def greet(ctx):
	"""Greets you."""
	await ctx.send("boyyoass")

@bot.group(hidden=True)
@commands.has_role('Owners')
async def config(ctx):
	"""Configuration commands. Only tatan can access them."""
	if ctx.author.id == tatanID:
		if ctx.invoked_subcommand is None:
			await ctx.send("no subcommand was called")
	else:
		await ctx.send("don\'t fuckin touch my configs")

@config.command()
async def play(ctx, *, game: str):
	"""Changes the bot's "playing" status."""
	await ctx.send('now playing ' + game.lower())
	gameStat = discord.Game(game)
	await bot.change_presence(activity=gameStat)

@config.command()
async def stream(ctx, *, streaming: str):
	await ctx.send('now streaming ' + streaming.lower())
	streamStat = discord.Game(name=streaming, type=1, url='https://twitch.tv/tatanphnx')
	await bot.change_presence(activity=streamStat)

@config.command()
async def say(ctx, *, echo: str):
	await ctx.message.delete()
	await ctx.send(echo)

close_aliases = ['sleep', 'exit']
@config.command(aliases=close_aliases)
async def close(ctx):
	await ctx.send('ima go bye')
	exit()

bot.run(token)
