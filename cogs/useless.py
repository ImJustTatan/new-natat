import discord
from discord.ext import commands as bot
import random

class Fun:
	def __init__(self, bot):
		self.bot = bot

	@bot.command(description='A simple command for testing the bot.', 
					  aliases=['hello', 'salute', 'test'])
	async def greet(ctx):
		"""Greets you. Mainly used for testing."""
		await ctx.send(random.choice(["boyyoass", "heyo", "what do you want"]))

	@bot.command()
	@bot.guild_only()
	async def joined(self, ctx, *, member: discord.Member):
		"""Says when a member joined."""
		await ctx.send(f'{member.display_name} joined on {member.joined_at}')

def setup(bot):
	bot.add_cog(Fun(bot))