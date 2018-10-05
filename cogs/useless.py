import discord
from discord.ext import commands
import random

import wikipedia
import pokebase as pb

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
		wiki_lang = language
		wikipedia.set_lang(language)
		if ctx.invoked_subcommand is None:
			error_d = 'this is a fuckin subcommand, idiot. can\'t you just do !help wp or something?'
			await ctx.send(embed=error_embed(error_d))
			
	@wikipedia.command(aliases=['a','page'])
	async def article(self, ctx, article_name: str):
		"""Shows an article from the provided name."""
		article_obj = wikipedia.suggest(article_name)
		if article_obj is None:
			error_d = f'no page returned with "{article_name.lower()}", check your spelling or something.'
			await ctx.send(embed=error_embed(error_d))
		else:
			article_em = discord.Embed(title=article_obj.title,colour=ctx.author.colour,url=article_obj.url)
			
			article_em.set_author(name=f'requested by {ctx.author.name}',icon_url=ctx.author.avatar_url)
			article_em.set_image(article_obj.images[0])
			
			article_em.add_field(name='Summary:', value=article_obj.summary, inline=False)
			category_str = ', '.join(article_obj.categories)
			article_em.add_field(name='Categories:', value=category_str)
			
			global wiki_lang
			article_em.set_footer(text=f'current language: {wiki_lang}', icon_url=self.bot.user.avatar_url)
			
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
		
	# pokemon
	
	@commands.command(aliases=['pokemon','pokebase'])
	async def pokedex(self, ctx, id = None):
		"""Retrieves a Pokémon with info."""
		if id is None:
			error_d = 'specify a pokemon you fuck'
			await ctx.send(embed=error_embed(error_d))
		else:
			pdmon = pb.pokemon(id)
			pdex_title = f'Pokédex Entry'
			pdex_desc = f'pokédex info on the pokémon {pdmon.name}'
			
			pdex_em = discord.Embed(title=pdex_title,colour=ctx.author.colour)
			pdex_em.set_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pdmon.id}.png')
			pdex_em.add_field(name='Entry:',value=f'#{pdmon.id}')
			pdex_em.add_field(name='Type:',value=pb.type_(pdmon.id))
			pdex_em.add_field(name='Height:',value=f'{pdmon.height}ft.')
			
			await ctx.send(embed=pdex_em)

def setup(bot):
	bot.add_cog(Fun(bot))