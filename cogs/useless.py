"""Pretty much useless commands. Just junk."""
import discord
from discord.ext import commands
import random

class Fun:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description='A simple command for testing the bot.', 
					  aliases=['hello', 'salute', 'test'])
	async def greet(ctx):
		"""Greets you. Mainly used for testing."""
		await ctx.send(random.choice(["boyyoass", "heyo", "what do you want"]))

	@commands.command(name='8ball',description=
								  'Gives out a random choice between many user-given strings.\n'+
								  'Closing two or more words in quotes will count as one string.\n'+
								  '\nFor example: !8ball a b c will give a random choice between '+
								  '"a", "b" and "c". !8ball "a b" c  will give a random choice '+
								  'between the strings "a b" and "c".',
					  aliases=['choices', 'rng', 'random'])
	async def eightball(ctx, *args):
		"""Gives out a random choice between user-given strings. [BROKEN]"""
		choices = list(args)
		await ctx.send(random.choice(choices))

def setup(bot):
	bot.add_cog(Fun(bot))
