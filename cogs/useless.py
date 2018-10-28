import discord
from discord.ext import commands
import aiohttp

from useful import error_embed, str_limit

import random
from io import BytesIO

class Fun:
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)
		
	@commands.command(aliases=['randomcat'])
	async def cat(self, ctx):
		async with ctx.channel.typing():
			try:
				async with self.session.get('https://aws.random.cat/meow') as data:
					img_data = json.loads(data)
					async with self.session.get(img_data["file"]) as resp:
						buffer = BytesIO(await resp.read())
						img_obj = discord.File(fp=buffer, filename='cat.png')
						await ctx.send(content='meow', file=img_obj)
			except Exception as e:
				error_d = str_limit(str(e)))
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
	@eightball.error
	async def eightball_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send('there was an error')

	@commands.command(aliases=['rng','pick'])
	async def dice(self, ctx, none: int = 1, ntwo: int = 6):
		"""A dice with custom numbers."""
		await ctx.send(f'your lucky number is {random.randint(none, ntwo)}')

def setup(bot):
	bot.add_cog(Fun(bot))