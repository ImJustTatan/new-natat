import discord

def error_embed(error_desc: str, error_title: str = 'an error occured'):
	"""Returns an error-themed Embed. Basically just a shortcut."""
	return discord.Embed(title=error_title,description=error_desc,colour=0xe74c3c)

def docstring_parameter(*sub):
	"""useful function for using variables in docstrings
	i.e. @docstring_parameter(fyou)"""
	def dec(obj):
		obj.__doc__ = obj.__doc__.format(*sub)
		return obj
	return dec

def str_limit(og_str: str, limit: int = 1021):
	"""returns an embed-friendly string with 1024 characters (or more if provided).
	returns the original string if its length is less than the limit."""
	return (og_str[:limit] + '...') if len(og_str) > limit else og_str
