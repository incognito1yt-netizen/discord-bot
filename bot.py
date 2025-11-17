from dotenv import load_dotenv
load_dotenv()
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True  # wymagane dla on_member_join
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Ładowanie wszystkich cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def setup_hook():
    await load_cogs()
    await bot.tree.sync()  # synchronizacja slash commands

import os
TOKEN = os.getenv("DISCORD_TOKEN")
