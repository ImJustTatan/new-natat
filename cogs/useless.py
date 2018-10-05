import discord
from discord.ext import commands
import random

import wikipedia
import pokebase as pb

def error_embed(error_desc: str, error_title: str = 'an error occured'):
	"""Returns an error-themed Embed. Basically just a shortcut."""
	return discord.Embed(title=error_title,description=error_desc,colour=0xe74c3c)

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
	async def wikipedia(self, ctx):
		if ctx.invoked_subcommand is None:
			error_d = 'this is a fuckin subcommand, idiot. can\'t you just do !help wp or something?'
			await ctx.send(embed=error_embed(error_d))
			
	@wikipedia.command(aliases=['s','find'])
	async def search(self, ctx, *, user_search: str = 'null', result_limit: int = 10):
		if user_search is 'null':
			error_d = 'uhh will you search for something or what.'
			await ctx.send(embed=error_embed(error_d))
		else:
			search_results = wikipedia.search(user_search,results=result_limit)
			
			counter = 0
			res_content = 'results:\n'
			for s_result in search_results:
				counter += 1
				res_content += f'\n{counter}.- {s_result.lower()}'
			await ctx.send(res_content)
		
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