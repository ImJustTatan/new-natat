import os # for env vars
import discord
from discord.ext import commands
from random import choice

import sys, traceback

initial_extensions = ['cogs.config']

tatanID = 119205994579492864
adminID = 494693989853954048
guildID = 290144092841836556

token = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix='!', owner_id=tatanID, description='tatan\'s bot.')

if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print(f'Failed to load extension {extension}.', file=sys.stderr)
			traceback.print_exc()

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
	await ctx.send(choice(["boyyoass", "heyo", "what do you want"]))

bot.run(token)
