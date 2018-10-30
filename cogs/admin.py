import discord
from discord.ext import commands

from useful import error_embed

class Administration:
	def __init__(self, bot):
		self.bot = bot
		
	@commands.group(hidden=True, case_insensitive=True)
	@commands.has_role('Admins')
	async def admin(self, ctx):
		"""Admin commands. Useful for quickly administrating."""
		if ctx.invoked_subcommand is None:
			error_d = 'you either didn\'t pass any command or you wrote some fuckin typo'
			await ctx.send(embed=error_embed(error_d))

	@commands.group(hidden=True, case_insensitive=True)
	@commands.has_role('Mods')
	async def mod(self, ctx):
		"""Moderation commands. Quick shortcuts for moderating stuff."""
		if ctx.invoked_subcommand is None:
			error_d = 'you either didn\'t pass any command or you wrote some fuckin typo'
			await ctx.send(embed=error_embed(error_d))

	@admin.command()
	async def ban(self, ctx, member: discord.Member = None, reason: str = None):
		"""Bans a member. You can optionally provide a reason after the mention."""
		async with ctx.channel.typing():
			if member is not None:
				await member.ban(reason=reason)
				await ctx.send('done')
			else:
				error_d = 'mention the user dumbass'
				await ctx.send(embed=error_embed(error_d))

	@mod.command(aliases=['massdelete'])
	async def purge(self, ctx, limit: int = 100, reverse: bool = False):
		"""Purges a given number of messages."""
		async with ctx.channel.typing():
			await ctx.channel.purge(limit=limit, reverse=reverse)
			await ctx.send(f'purged {limit} messages')

	@mod.command()
	async def kick(self, ctx, member: discord.Member = None, reason: str = None):
		"""Kicks a member. You can optionally provide a reason after the mention."""
		async with ctx.channel.typing():
			if member is not None:
				await member.kick(reason=reason)
				await ctx.send('done')
			else:
				error_d = 'mention the user dumbass'
				await ctx.send(embed=error_embed(error_d))
			
def setup(bot):
	bot.add_cog(Administration(bot))
