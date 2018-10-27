import discord
from discord.ext import commands

from useful import error_embed

class Configurations:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name='config', pass_context=True,
			  aliases=['conf', 'cf', 'settings', 'set'])
	@commands.has_role('Owner')
	async def config(self, ctx):
		"""Configuration commands. Only the Owners can access them."""
		if ctx.invoked_subcommand is None:
			error_d = "no subcommand was called"
			await ctx.send(embed=error_embed(error_d))

	@commands.group(aliases=['db','dbg'])
	@commands.is_owner()
	async def debug(self, ctx):
		"""Debug commands for debugging bugs."""
		if ctx.invoked_subcommand is None:
			error_d = "no debug command was called"
			await ctx.send(embed=error_embed(error_d))

	@config.command()
	async def play(self, ctx, *, game: str = 'help'):
		"""Changes the bot's "playing" status."""
		await ctx.send('now playing ' + game.lower())
		gameStat = discord.Game(game)
		await self.bot.change_presence(activity=gameStat)
		
	@config.command()
	async def stream(self, ctx, *, game: str = '!help', url: str = 'https://twitch.tv/tatanphnx'):
		"""Changes the bot's "streaming" status."""
		streamStat = discord.Streaming(game, url)
		await self.bot.change_presence(activity=streamStat)

	@config.command(aliases=['echo', 'reply'])
	async def say(self, ctx, *, message: str):
		"""Makes the bot say <message>."""
		await ctx.message.delete()
		await ctx.send(message)

	@config.command(aliases=['cl','sleep', 'exit'])
	async def close(self, ctx):
		"""Shuts down the bot."""
		await ctx.send('ima go bye')
		exit()

	@debug.command(aliases=['load'])
	async def cog_load(self, ctx, *, cog: str):
		"""Loads a module/cog."""
		self.bot.load_extension(cog)

	@debug.command(aliases=['unload'])
	async def cog_unload(self, ctx, *, cog: str):
		"""Unloads a module/cog."""
		self.bot.unload_extension(cog)

def setup(bot):
	bot.add_cog(Configurations(bot))