# bot.py
import os
import random
import asyncio
import logging
import sys
import json

import discord
import nacl

from dotenv import load_dotenv
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp
from easypydb import DB


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = """A bot meant to be a learning tool for Python and bot creation.
                Eventually will made into a feature heavy FFXIV/General admin bot."""

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TOKENDB = os.getenv('TOKENDB')
database = DB("HoloCount", TOKENDB)

menu = DefaultMenu('◀️', '▶️', '❌', active_time=15)

global holo_count
holo_count = 0

bot = commands.Bot(
    command_prefix='$',
    description=description,
    intents=intents,
    owner_id=172476429081116673,
    case_insensitive=True
)
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green())

extensions = (
    'plugins.music',
    'plugins.admin',
    'plugins.destroy',
    'plugins.wikipedia',
    'plugins.fun',
    #'plugins.economy'
)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    #bot.remove_command('help')
    for extension in extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f"Couldn't load the following extension: {extension}; {e}", file=sys.stderr)
    return

# Sends a message to the user if they don't have the correct role for a command.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

# Creates a new DM channel to welcome new members.
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to {discord.Guild}!')


@bot.event
async def on_message(message):
    if message.content.startswith('holocaust'):
        global holo_count
        holo_count += 1
        emb = discord.Embed(
            title = f'Holocaust Count: ',
            description = f'The holo count is now: {holo_count}',
            color = discord.Colour.green()
        )
        await message.channel.purge(limit=1)
        await message.channel.send(embed=emb, delete_after=10)
    break

bot.run(TOKEN, bot=True, reconnect=True)
