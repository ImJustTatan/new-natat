import discord
from discord.ext import commands

class Configurations:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name='config', aliases=['conf', 'settings', 'set'])
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
		"""Changes the bot's "playing" status. [BROKEN]"""
		await ctx.send('now streaming ' + streaming.lower())
		streamStat = discord.Game(name=streaming, type=1, url='https://twitch.tv/tatanphnx')
		await bot.change_presence(activity=streamStat)

	@config.command(aliases=['echo', 'reply'])
	async def say(ctx, *, message: str):
		"""Makes the bot say <message>."""
		await ctx.message.delete()
		await ctx.send(message)

	@config.command(aliases=['sleep', 'exit'])
	async def close(ctx):
		"""Shuts down the bot."""
		await ctx.send('ima go bye')
		exit()

def setup(bot):
bot.add_cog(Configurations(bot))
