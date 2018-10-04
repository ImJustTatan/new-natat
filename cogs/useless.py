import discord
from discord.ext import commands
import random
import pokebase as pb

class Fun:
	def __init__(self, bot):
		self.bot = bot
		
	# fun stuff

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
		
	# apis and stuff
	
	@commands.command(aliases=['pokemon','pokebase'])
	async def pokedex(self, ctx, id = None):
		if id is None:
			error_desc = 'specify a pokemon you fuck'
			error_msg = discord.Embed(title='an error occured',description=error_desc,colour=0xe74c3c)
			ctx.send(embed=error_msg)
		else:
			pdmon = pb.pokemon(id)
			pdex_title = f'Pokédex Entry: {pdmon.name}'
			pdex_thumb = pb.SpriteResource('pokemon',id)
			
			pdex_em = discord.Embed(title=pdex_title,colour=0x1f8b4c)
			pdex_em.set_thumbnail(pdex_thumb.url)
			pdex_em.add_field('Entry:',f'#{pdmon.id}')
			pdex_em.add_field('Type:',pdmon.type)
			pdex_em.add_field('Height:',f'{pdmon.height}ft.')
			
			ctx.send(embed=pdex_em)

def setup(bot):
	bot.add_cog(Fun(bot))