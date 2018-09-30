"""
Base code provided by EvieePy: https://gist.github.com/EvieePy/ab667b74e9758433b3eb806c53a19f34
"""

import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

thdown = '\U0001F44E'
thup = '\U0001F44D'

ydl = YoutubeDL()
ydl.add_default_info_extractors()
class Music:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def join(self, ctx):
		"""Joins the current voice channel. Mainly used for testing."""
		global thdown
		global thup

		voice_client = ctx.guild.voice_client
		if voice_client is None:
			await ctx.message.add_reaction(thup)
			voice_client = await ctx.author.voice.channel.connect()
		elif voice_client is discord.VoiceClient:
			await ctx.message.add_reaction(thdown)
			await ctx.send('i\'m in your voice channel already')
		else:
			await ctx.message.add_reaction(thdown)
			await ctx.send('some error occured, fuck off')

	@commands.command()
	async def leave(self, ctx):
		"""Leaves a voice chat if joined any."""
		global thdown
		global thup
		voice_client = ctx.guild.voice_client
		if voice_client is None:
			await ctx.message.add_reaction(thdown)
			await ctx.send('i must be connected to a voice channel for that to happen')
		else:
			await ctx.message.add_reaction(thup)
			await voice_client.disconnect()

	@commands.command()
	async def play(self, ctx, *, url: str):
		"""Plays a YouTube link."""
		voice_client = ctx.guild.voice_client
		if voice_client is None:
			voice_client = await ctx.author.voice.channel.connect()

		info = ydl.extract_info(url, download=False)
		source = ydl.prepare_filename(info)

		voice_client.play(discord.FFmpegPCMAudio(source, pipe=False))

def setup(bot):
	bot.add_cog(Music(bot))
