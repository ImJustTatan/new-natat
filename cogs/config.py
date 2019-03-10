import discord
from discord.ext import commands
import aiohttp

from useful import error_embed

import json
import random
import mimetypes
from io import BytesIO

with open('ids.json') as j:
	ids = json.load(j)

class Configurations:
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)

	@commands.group(name='config', hidden=True,
			  aliases=['conf', 'cf', 'settings', 'set'])
	@commands.has_role('Mechanics')
	async def config(self, ctx):
		"""Configuration commands. Only the Owners can access them."""
		if ctx.invoked_subcommand is None:
			error_d = "no subcommand was called"
			await ctx.send(embed=error_embed(error_d))

	@commands.group(aliases=['db','dbg'], hidden=True)
	@commands.has_role('Mechanics')
	async def debug(self, ctx):
		"""Debug commands for debugging bugs."""
		if ctx.invoked_subcommand is None:
			error_d = "no debug command was called"
			await ctx.send(embed=error_embed(error_d))

	@config.command()
	async def avatar(self, ctx, member: discord.Member = None):
		"""Changes the bot's avatar to that of the context's attachment."""
		async with ctx.typing():
			if member is None:
				attachments = ctx.message.attachments
				if attachments:
					avatar = random.choice(attachments)
					async with self.session.get(avatar.url) as resp:
						buffer = BytesIO(await resp.read())

						content_type = resp.headers['content-type']
						ext = mimetypes.guess_extension(content_type)

						if ext.endswith('jpe'):
							n_ext = '.jpeg'
						else:
							n_ext = ext

						avatar_file = discord.File(fp=buffer, filename=f'avatar{n_ext}')

						await self.bot.user.edit(avatar=await resp.read())
						await ctx.send('new avatar set to:', file=avatar_file)
				else:
					error_d = 'send an avatar idiot'
					await ctx.send(embed=error_embed(error_d))
			else:
				async with self.session.get(member.avatar_url_as(format='png')) as resp:
					buffer = BytesIO(await resp.read())
					avatar_file = discord.File(fp=buffer, filename='avatar.png')

					await self.bot.user.edit(avatar=await resp.read())
					await ctx.send(f'new avatar set to {member.display_name.lower()}\'s:', file=avatar_file)

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

	@commands.is_owner()
	@commands.command(aliases=['ds', 'ass'], hidden=True)
	async def dev_say(self, ctx, channel_name: str = str(ids['announcements']), 
			*, echo: str = None):
		"""Echoes a given message to the select text channels in ids.json."""
		if channel_name in ids and echo is not None:
			target_channel = self.bot.get_channel(ids[channel_name])
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
					
					await target_channel.send(echo, file=img_file)
			else:
				await target_channel.send(echo)
				
			await ctx.send("ok")

		elif channel_name not in ids or echo is None:
			if echo is None:
				error_d = error_embed('the fuck do i send dumbass')
			else:
				error_d = error_embed('specified channel is not in ids.json\
					\n tatan you dumb idiot')
			await ctx.send(embed=error_d)

	@commands.is_owner()
	@commands.command(aliases=['cl','sleep', 'exit'], hidden=True)
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