import discord
from discord.ext import commands

import os
import random

import wikipedia
import lyricsgenius as genius

genius_token = os.environ.get('GENIUS-TOKEN')
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
			ctx.send(embed=error_embed(error_d))
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
				
				article_em.set_author(name=f'requested by {ctx.author.name}',icon_url=ctx.author.avatar_url)
				article_obj_summary = wikipedia.summary(article_obj.title, sentences=2)
				article_em.add_field(name='Summary:', value=article_obj_summary, inline=False)
				global wiki_lang
				article_em.set_footer(text=f'current language: {wiki_lang}', icon_url=self.bot.user.avatar_url)
				article_em.set_image(url=random.choice(article_obj.images))

				await ctx.send(embed=article_em)
			
	@wikipedia.command(aliases=['s','find'])
	async def search(self, ctx, *, user_search: str = 'null', result_limit: int = 10):
		"""Wikipedia article searcher."""
		if user_search is 'null':
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
			res_content.set_author(name=f'requested by {ctx.author.name}',icon_url=ctx.author.avatar_url)
			res_content.set_footer(text=f'choose an article to show. | current language: {wiki_lang}', icon_url=self.bot.user.avatar_url)
			await ctx.send(embed=res_content)

	@commands.group(aliases=['lyrics'])
	async def genius(self, ctx):
		"""For interacting with genius.com. Do !help genius."""
		error_d = 'under construction'
		await ctx.send(embed=error_embed(error_d))

def setup(bot):
	bot.add_cog(Fun(bot))