import discord
from discord.ext import commands
import aiohttp

from useful import error_embed, str_limit

import json
import random
import mimetypes
from io import BytesIO

with open('ids.json') as j:
	ids = json.load(j)

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)

	@commands.command(aliases=['number'])
	async def number_fact(self, ctx, number: str = 'random'):
		"""Returns a random fact about a number.
		You can optionally provide a number to return a fact from"""
		async with ctx.channel.typing():
			async with self.session.get(f'http://numbersapi.com/{number}') as resp:
				await ctx.send(await resp.text())
	
	@commands.command(aliases=['randomcat'])
	async def cat(self, ctx, format: str = None):
		"""Returns a random image of a cat.
		You can optionally provide a format."""
		async with ctx.channel.typing():
			formats = ['png', 'jpg', 'gif']
			if format is None:
				format = random.choice(formats)
			if format in formats:
				url = f'http://thecatapi.com/api/images/get?type={format}'
				async with self.session.get(url) as resp:
					buffer = BytesIO(await resp.read())
					img = discord.File(fp=buffer, filename=f'cat.{format}')
					await ctx.send(content='meow',file=img)
			else:
				error_d = f'"{format}" is not a valid format, dumbass.'
				await ctx.send(embed=error_embed(error_d))

	@commands.command(description='A simple command for testing the bot.', 
			    aliases=['hello', 'salute', 'test'])
	async def greet(self, ctx):
		"""Greets you. Mainly used for testing."""
		await ctx.send(random.choice(["boyyoass", "heyo", "what do you want"]))

	@commands.command(name='8ball', aliases=['random','choose','choice'])
	async def eightball(self, ctx, *args):
		"""Chooses between infinite number of arguments."""
		await ctx.send(random.choice(args))

	@commands.command(aliases=['rng','pick'])
	async def dice(self, ctx, none: int = 1, ntwo: int = 6):
		"""A dice with custom numbers."""
		await ctx.send(f'your lucky number is {random.randint(none, ntwo)}')

	@commands.command(aliases=['naenae'])
	async def dab(self, ctx):
		"""*dabs*"""
		mojis = ctx.guild.emojis
		moji = random.choice(mojis)
		await ctx.send(f'{moji} dab!!!')

	@commands.command(aliases=['yeet'])
	async def dance(self, ctx):
		"""*dances*"""
		moji_guild = self.bot.get_guild(ids["guild-test"])
		mojis = moji_guild.emojis
		moji = random.choice(mojis)
		statement = random.choice(['yeet', 'dance'])
		await ctx.send(f'{moji} {statement}!!!!!')

def setup(bot):
	bot.add_cog(Fun(bot))