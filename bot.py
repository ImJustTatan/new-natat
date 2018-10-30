import discord
from discord.ext import commands

import os # for env vars
import random
import asyncio
import sys, traceback
import json

initial_extensions = ['cogs.config',
			 'cogs.members',
			 'cogs.useless',
			 'cogs.apis',
			 'cogs.admin']

tatanID = 119205994579492864
adminID = 504803538518671374

guildID = 504412544673251337
generalID = 504412545134886923

token = os.environ.get('TOKEN')
if token is None:
	with open('config.json') as j:
		config = json.load(j)
		token = config['token']

def get_prefix(bot, message):
	"""Callable prefix function. [TODO] Can be modified at will."""
	prefixes = ['>', '!','.']
	if not message.guild:
		return ''
	return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, owner_id=tatanID, 
				   description='i\'m natat and i am suffering every second i\'m on')

for extension in initial_extensions:
	bot.load_extension(extension)

tatan = bot.get_user(tatanID)
general = bot.get_channel(generalID)

cpasta = os.environ.get('COPYPASTA')
if cpasta is None:
	with open('config.json') as j:
		config = json.load(j)
		token = config['token']
		cpasta = config['copypasta']

fyou = ['fuck off', 'fuck you',
	 'stop it', 'im gonna kill you',
	 'that\'s fuckin illegal man',
	 'can you not', 'STOP', cpasta]

illegal_words = [':v', 'nigger', 'faggot', 'soyboy',
		   'v:', 'kek', 'soy boy' 'soy boi',
		   'soyboi', 'fagget', '>mfw', '>tfw',
		   'soi boi']

motd = ['A'*7,'tatan shut me down','how i had die']

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
	bot.loop.create_task(status_task())
	
@bot.event
async def on_member_join(member):
	if 'discord.gg' in member.name.lower():
		await member.ban(reason='spambot')
	else:
		welcome_message = f'hello {member.name.lower()} and welcome to tatan\'s server. read the law and have fun.'
		await member.send(welcome_message)
		
@bot.event
async def on_member_remove(member):
	general.send(f'`{str(member)}` left the server.')

@bot.event
async def on_message(msg):
	# word filter
	for word in illegal_words:
		if word in msg.content.lower():
			if msg.author != bot.user and msg.author != tatan:
				await msg.channel.send(random.choice([':gun:', ':knife:', ':dagger:']))
				await msg.author.send(random.choice(fyou))
				await msg.delete()
			else:
				pass
	
	await bot.process_commands(msg)

bot.run(token)