import discord
from discord.ext import commands
import random

class Fun:
	def __init__(self, bot):
		self.bot = bot

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
