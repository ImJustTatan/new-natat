import discord
from discord.ext import commands
import random

class Members:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['joinedat', 'joined_at'])
	@commands.guild_only()
	async def joined(self, ctx, *, member: discord.Member):
		"""Says when a member joined."""
		if member != ctx.author:
			await ctx.send(f'{member.display_name} joined on {member.joined_at}')

	@commands.command(aliases=['pfp', 'profilepic', 'avatarpic', 
				      'pic', 'userpic'])
	async def avatar(self, ctx, *, member: discord.Member):
		"""Messages a member's avatar url back."""
		if member != ctx.author:
			await ctx.send(content=f'here\'s {member.display_name}\'s uglyass avatar {member.avatar_url}')
def setup(bot):
	bot.add_cog(Members(bot))
