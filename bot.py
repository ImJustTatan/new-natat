import os # for env vars
import discord
from discord.ext import commands
import random
import asyncio

import sys, traceback

initial_extensions = ['cogs.config',
			 'cogs.members',
			 'cogs.useless']

tatanID = 119205994579492864
adminID = 494693989853954048
guildID = 290144092841836556

token = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix='!', owner_id=tatanID, 
				   description='i\'m natat and i am suffering every second i\'m on')

for extension in initial_extensions:
	bot.load_extension(extension)

tatanID = bot.get_user(tatanID)

fyou = ['fuck off', 'fuck you',
	 'stop it', 'im gonna kill you',
	 'that\'s fuckin illegal man',
	 'can you not', 'STOP']

illegal_words = [':v', 'nigger', 'faggot', 'soyboy',
		   'v:', 'kek', 'soy boy' 'soy boi',
		   'soyboi', 'fagget', '>mfw', '>tfw',
		   'soi boi']

motd = ['A'*7,'tatan shut me down','how i had die']

def docstring_parameter(*sub):
	"""useful function for using variables in docstrings
	i.e. @docstring_parameter(fyou)"""
	def dec(obj):
		obj.__doc__ = obj.__doc__.format(*sub)
		return obj
	return dec

async def status_task(sec=1200):
	"""Changes status every X seconds."""
	while True:
		gameStat = discord.Game(f'!help | {random.choice(motd)}')
		await bot.change_presence(activity=gameStat)
		await asyncio.sleep(int(sec))

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	bot.loop.status_task()
	
@bot.event
async def on_member_joined(member):
	if 'discord.gg' in member.name.lower():
		await member.ban(reason='spambot')
	else:
		welcome_message = f'hello {member.name.lower()} and welcome to hr285\'s (aka tatan) server. read the law and have fun.'
		await member.send(welcome_message)
	
@bot.event
async def on_message(msg):
	# word filter
	for word in illegal_words:
		if word in msg.content.lower():
			if msg.author != bot.user:
				await msg.channel.send(random.choice([':gun:', ':knife:', ':dagger:']))
				await msg.author.send(random.choice(fyou))
				await msg.delete()
			else:
				pass
	
	await bot.process_commands(msg)

bot.run(token)