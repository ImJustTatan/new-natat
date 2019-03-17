import discord
from discord.ext import commands
import aiohttp

from useful import error_embed

from io import BytesIO
import mimetypes
import random
import json

with open('ids.json') as j:
	ids = json.load(j)

class Members(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)

	@commands.command(aliases=['joinedat', 'joined_at'])
	@commands.guild_only()
	async def joined(self, ctx, *, member: discord.Member = None):
		"""Says when a member joined."""
		if member is None:
			joined_at = str(ctx.author.joined_at)[:-7]
			await ctx.send(f'you joined on `{joined_at}`')
		else:
			joined_at = str(member.joined_at)[:-7]
			await ctx.send(f'{member.display_name} joined on `{joined_at}`')

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

	@commands.command(aliases=['dick', 'm'])
	async def tmail(self, ctx, *, echo: str = None):
		"""Sends a message directly to tatan :)."""
		tatan = self.bot.get_user(ids["tatan"])
		attachments = ctx.message.attachments
		if attachments:
			img = random.choice(attachments)
			async with self.session.get(img.url) as resp:
				buffer = BytesIO(await resp.read())

				content_type = resp.headers['content-type']
				ext = mimetypes.guess_extension(content_type)

				if ext.endswith('jpe'):
					n_ext = '.jpeg'
				elif ext.endswith('mp2'):
					n_ext = '.mp3'
				else:
					n_ext = ext

				img_file = discord.File(fp=buffer, filename=f'attached{n_ext}')
				
				if echo is not None:
					await tatan.send(f'{echo}\n`sent by {ctx.author.display_name} in {ctx.channel.name}`', 
							file=img_file)
				else:
					await tatan.send(f'`sent by {ctx.author.display_name} in {ctx.channel.name}`', 
							file=img_file)
				await ctx.send(':+1: mailed to tatan :)')
				
		elif not attachments and echo is None:
			error_d = error_embed('can you uh gimme a message or an image or somethin\'')
			await ctx.send(embed=error_d)
		else:
			await tatan.send(f'{echo}\n`sent by {ctx.author.display_name} in {ctx.channel.name}`')
			await ctx.send(':+1: mailed to tatan :)')

def setup(bot):
	bot.add_cog(Members(bot))