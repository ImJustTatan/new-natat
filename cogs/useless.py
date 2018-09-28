import discord
from discord.ext import commands
import random

class Fun:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description='A simple command for testing the bot.', aliases=['hello', 'salute', 'test'])
	async def greet(ctx):
		"""Greets you. Mainly used for testing."""
		await ctx.send(random.choice(["boyyoass", "heyo", "what do you want"]))

def setup(bot):
	bot.add_cog(Fun(bot))