import discord
from discord.ext import commands
import os
from bot import token

bot = commands.Bot(command_prefix='!')
await bot.close()

bot.run(token)
