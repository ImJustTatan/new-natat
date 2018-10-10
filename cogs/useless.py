import discord
from discord.ext import commands

import os
import random
import json

import wikipedia
import lyricsgenius as genius

genius_token = os.environ.get('GENIUS-TOKEN')
if genius_token is None:
	with open('config.json') as j:
		config = json.load(j)
		genius_token = config['genius_token']
genius_api = genius.Genius(genius_token)

def error_embed(error_desc: str, error_title: str = 'an error occured'):
	"""Returns an error-themed Embed. Basically just a shortcut."""
	return discord.Embed(title=error_title,description=error_desc,colour=0xe74c3c)

wiki_lang = 'en'

class Fun:
	def __init__(self, bot):
		self.bot = bot
		
	### fun stuff

	@commands.command(description='A simple command for testing the bot.', 
			    aliases=['hello', 'salute', 'test'])
	async def greet(self, ctx):
		"""Greets you. Mainly used for testing."""
		await ctx.send(random.choice(["boyyoass", "heyo", "what do you want"]))

	@commands.command(name='8ball', aliases=['random','choose','choice'])
	async def eightball(self, ctx, *args):
		"""Chooses between infinite number of arguments."""
		await ctx.send(random.choice(args))
	@eightball.error
	async def eightball_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send('there was an error')

	@commands.command(aliases=['rng','pick'])
	async def dice(self, ctx, none: int = 1, ntwo: int = 6):
		"""A dice with custom numbers."""
		await ctx.send(f'your lucky number is {random.randint(none, ntwo)}')
		
	### apis and stuff
	# wikipedia
	
	@commands.group(aliases=['wiki','wp'])
	async def wikipedia(self, ctx, language: str):
		"""Wikipedia based command. Do !help wp."""
		global wiki_lang
		if language in wikipedia.languages():
			wiki_lang = language
			wikipedia.set_lang(language)
		else:
			error_d = f'"{language}" isn\'t in the list of languages.'
			await ctx.send(embed=error_embed(error_d))
		if ctx.invoked_subcommand is None:
			error_d = 'this is a fuckin subcommand, idiot. can\'t you just do !help wp or something?'
			await ctx.send(embed=error_embed(error_d))
			
	@wikipedia.command(aliases=['a','p','article'])
	async def page(self, ctx, *, article_name: str):
		"""Shows an article from the provided name."""
		article_obj = wikipedia.page(article_name)
		if article_obj is None:
			error_d = f'no page returned with "{article_name.lower()}", check your spelling or something.'
			await ctx.send(embed=error_embed(error_d))
		else:
			async with ctx.channel.typing():
				article_em = discord.Embed(title=article_obj.title,colour=ctx.author.colour,url=article_obj.url)
				
				article_em.set_author(name=f'requested by {ctx.author.name.lower()}',icon_url=ctx.author.avatar_url)
				article_obj_summary = wikipedia.summary(article_obj.title, sentences=2)
				article_em.add_field(name='Summary:', value=article_obj_summary, inline=False)
				global wiki_lang
				article_em.set_footer(text=f'current language: {wiki_lang}', icon_url=self.bot.user.avatar_url)
				article_em.set_image(url=random.choice(article_obj.images))

				await ctx.send(embed=article_em)
			
	@wikipedia.command(aliases=['r'])
	async def random(self, ctx):
		"""[BROKEN] Sends a random article from Wikipedia."""
		article_obj = wikipedia.random()
		async with ctx.channel.typing():
			article_em = discord.Embed(title=article_obj.title,colour=ctx.author.colour)
			
			article_em.set_author(name=f'requested by {ctx.author.name.lower()}',icon_url=ctx.author.avatar_url)
			article_obj_summary = wikipedia.summary(article_obj.title, sentences=2)
			article_em.add_field(name='Summary:', value=article_obj_summary, inline=False)
			global wiki_lang
			article_em.set_footer(text=f'current language: {wiki_lang}', icon_url=self.bot.user.avatar_url)
			article_em.set_image(url=random.choice(article_obj.images))

			await ctx.send(embed=article_em)

	@wikipedia.command(aliases=['s','find'])
	async def search(self, ctx, *, user_search: str = "", result_limit: int = 10):
		"""Wikipedia article searcher."""
		if user_search is "":
			error_d = 'uhh will you search for something or what.'
			await ctx.send(embed=error_embed(error_d))
		else:
			search_results = wikipedia.search(user_search,results=result_limit)
			
			counter = -1
			res_content = discord.Embed(title=f'Results for {user_search}:',colour=ctx.author.colour)
			for s_result in search_results:
				counter += 1
				res_content.add_field(name=f'result #{counter}',value=f'{s_result}',inline=False)
			global wiki_lang
			res_content.set_author(name=f'requested by {ctx.author.name.lower()}',icon_url=ctx.author.avatar_url)
			res_content.set_footer(text=f'choose an article to show. | current language: {wiki_lang}', icon_url=self.bot.user.avatar_url)
			await ctx.send(embed=res_content)

	@commands.group(aliases=['g'])
	async def genius(self, ctx):
		"""For interacting with genius.com. Do !help genius."""
		if ctx.invoked_subcommand is None:
			error_d = 'ask tatan or something'
			await ctx.send(embed=error_embed(error_d))

	@genius.command(aliases=['s', 'lyrics'])
	async def song(self, ctx, *, song_name: str = ""):
		"""Searches a song and returns the lyrics."""
		if song_name is "":
			error_d = 'no search term was passed, asshat'
			await ctx.send(embed=error_embed(error_d))
		else:
			async with ctx.channel.typing():
				song_obj = genius_api.search_song(song_name)
				if song_obj is None:
					error_d = f'no song was found with the name "{song_name.lower()}"'
					await ctx.send(embed=error_embed(error_d))
				else:
					song_em = discord.Embed(title=song_obj.title,url=song_obj.url,colour=ctx.author.colour)
					song_em.set_author(name=f'requested by {ctx.author.name.lower()}', icon_url=ctx.author.avatar_url)
					
					song_cover = song_obj.song_art_image_url
					song_em.set_thumbnail(url=song_cover)

					song_em.add_field(name='artist',value=song_obj.artist)
					song_em.add_field(name='album', value=song_obj.album,inline=False)
					song_em.add_field(name='year',value=song_obj.year)

					song_lyrics = (song_obj.lyrics[:1021] + '...') if len(song_obj.lyrics) > 1021 else song_obj.lyrics
					song_em.add_field(name='lyrics',value=song_lyrics,inline=False)

					song_em.set_footer(text='click the song\'s url for more info',icon_url=self.bot.user.avatar_url)

					await ctx.send(embed=song_em)

	@genius.command(aliases=['a'])
	async def artist(self, ctx, *, artist_name: str = ""):
		"""Returns info about a certain given artist."""
		if artist_name is "":
			error_d = 'you could uh, pass an artist\'s name to do that maybe?'
			ctx.send(embed=error_embed(error_d))
		else:
			async with ctx.channel.typing():
				artist_obj = genius_api.search_artist(artist_name, max_songs=1)
				if artist_obj is None:
					error_d = f'i didn\'t find any artist named "{artist_name.lower()}"'
					await ctx.send(embed=error_embed(error_d))
				else:
					artist_em = discord.Embed(title=artist_obj.name,colour=ctx.author.colour)
					artist_em.set_author(name=f'requested by {ctx.author.name.lower()}', icon_url=ctx.author.avatar_url)

					artist_img = artist_obj.image_url
					artist_em.set_image(url=artist_img)

					artist_song = artist_obj.songs
					artist_em.add_field(name='most viewed song lyrics', value=artist_song[0].title)

					artist_em.set_footer(text='check genius.com for more info',icon_url=self.bot.user.avatar_url)

					await ctx.send(embed=artist_em)

def setup(bot):
	bot.add_cog(Fun(bot))