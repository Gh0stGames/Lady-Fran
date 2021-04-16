from discord.ext import commands
from easypydb import DB
from dotenv import load_dotenv
import random
import discord
import os

TOKENDB = os.getenv('TOKENDB')
database = DB("MoneyDB", TOKENDB)

class Basic(commands.Cog):
    """Contains all basic commands."""
    def __init__(self, bot):
        self.bot = bot

# Commands that are just for fun.
    @commands.command(name='fft', help='Responds with a random quote from Final Fantasy Tactics')
    async def fft_command(self, ctx):
        fft_quotes = [
            'Names don\'t matter. What\'s important is how you live your life.',
            'A \'heretic\' coming to church... pretty bold...',
            (
                'Ignorance itself is a crime!'
            ),
        ]
        response = random.choice(fft_quotes)
        await ctx.send(response)

    @commands.command(name='roll', help='Rolls dice in NdN format')
    async def roll_command(self, ctx, dice: str):
        # Rolls a dice in NdN format.
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(name='add', help='Adds two numbers together.')
    async def add(self, ctx, left: int, right: int):
        await ctx.send(left + right)

# Commands that are more administrative in nature.
    @commands.command(name='create-channel', help='Allows an admin to create a new text channel.')
    @commands.has_role('Admin')
    async def create_channel(self, ctx, channel_name='Test-Channel'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)

    @commands.command(name='Clear', help='Clears a specified amount of previous text in channel.')
    @commands.has_role('Admin')
    async def clear(self, ctx, amount = 5):
        await ctx.channel.purge(limit = amount)
        await ctx.send(f'{ctx.message.author.mention} has cleared {amount} previous lines of text.')

    @commands.command(
        name='work',
        brief='Work and get some money!',
        help='Use this command to work and earn a random amount of money. Can be used once per hour.'
    )
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def _work(self, ctx):
        database.load()
        money = random.randint(1, 10)
        await ctx.send(f'{ctx.message.author.mention} worked really hard and earned ${money}!')
        try:
            balance = database[str(ctx.message.author.id)]
        except:
            balance = 0
        database[str(ctx.message.author.id)] = balance + money

    @_work.error
    async def _work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f'Hold yer horses, kid.',description=f'Try again in {error.retry_after:.2f}s.', color=discord.Colour.green())
            await ctx.send(embed=em)

    @commands.command(
        name='balance',
        brief='Check your balance',
        help='See the total amount of money that is in your balance'
    )
    async def _balance(self, ctx):
        database.load
        try:
            balance = database[str(ctx.message.author.id)]
        except:
            balance = 0
        await ctx.send(f'{ctx.message.author.mention}\'s total balance is ${balance}')

def setup(bot):
    bot.add_cog(Basic(bot))
