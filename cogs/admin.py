import discord
from discord.ext import commands

from useful import error_embed

class Administration:
	def __init__(self, bot):
		self.bot = bot
		
	@commands.group(hidden=True)
	@commands.has_role('Admins')
	async def admin(self, ctx):
		"""Admin commands. Useful for quickly administrating."""
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

	@admin.command()
	async def kick(self, ctx, member: discord.Member = None, reason: str = None):
		"""Kicks a member. You can optionally provide a reason after the mention."""
		async with ctx.channel.typing():
			if member is not None:
				await member.kick(reason=reason)
				await ctx.send('done')
			else:
				error_d = 'mention the user dumbass'
				await ctx.send(embed=error_embed(error_d))

	@admin.command(aliases=['giverole','giveroles'])
	async def role(self, ctx, member: discord.Member = None, *roles: discord.Role = None):
	"""Gives or removes roles from an user."""
	async with ctx.channel.typing():
		if member is not None:
			if roles is not None:
				for role in roles:
					if role in ctx.guild.roles:
						if role in member.roles:
							await member.remove_roles(role)
						else:
							await member.add_roles(role)
					else:
						error_d = f'"{str(role)}" is not a valid role.'
						await ctx.send(embed=error_embed(error_d))
				await ctx.send('done')
			else:
				error_d = 'mention the roles fuckass.'
				await ctx.send(embed=error_embed(error_d))
		else:
			error_d = 'specify an user.'
			await ctx.send(embed=error_embed(error_d))
		
	@admin.command(aliases=['massdelete'])
	async def purge(self, ctx, limit: int = 100, reverse: bool = False):
		"""Purges a given number of messages."""
		async with ctx.channel.typing()
			await ctx.channel.purge(limit=limit, reverse=reverse)
			await ctx.send('done')
			
def setup(bot):
	bot.add_cog(Administration(bot))
