# bot.py
import os, random, discord, asyncio, nacl, ffmpeg, youtube_dl, logging, keep_alive

from dotenv import load_dotenv
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''A bot meant to be a learning tool for Python and bot creation.

Eventually will made into a feature heavy FFXIV/General admin bot.
'''

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

menu = DefaultMenu('◀️', '▶️', '❌')

bot = commands.Bot(
    command_prefix='?',
    description=description,
    intents=intents,
    owner_id=172476429081116673,
    case_insensitive=True
)
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green())

cogs = ['cogs.basic','cogs.music']

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    #bot.remove_command('help')
    for cog in cogs:
        bot.load_extension(cog)
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
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

# Start the server
keep_alive.keep_alive()

# Login the bot
bot.run(TOKEN, bot=True, reconnect=True)
