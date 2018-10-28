import discord
from discord.ext import commands
import aiohttp

from io import BytesIO
import random

class Members:
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)

	@commands.command(aliases=['joinedat', 'joined_at'])
	@commands.guild_only()
	async def joined(self, ctx, *, member: discord.Member = None):
		"""Says when a member joined."""
		if member is None:
			await ctx.send(f'you joined on {ctx.author.joined_at - 9}')
		else:
			await ctx.send(f'{member.display_name} joined on {member.joined_at - 9}')

	@commands.command(aliases=['pfp', 'profilepic', 'avatarpic', 
				      'pic', 'userpic'])
	async def avatar(self, ctx, *, member: discord.Member = None):
		"""Messages a member's avatar url back."""
		if member is None:
			async with self.session.get(ctx.author.avatar_url) as resp:
				buffer = BytesIO(await resp.read())
				avatar = discord.File(fp=buffer, filename='avatar.webp')
				await ctx.send(content='here\'s your uglyass avatar', file=avatar)
		else:
			async with self.session.get(member.avatar_url) as resp:
				buffer = BytesIO(await resp.read())
				avatar = discord.File(fp=buffer, filename='avatar.webp')
				await ctx.send(content=f'here\'s {member.display_name}\'s uglyass avatar', file=avatar)

def setup(bot):
	bot.add_cog(Members(bot))