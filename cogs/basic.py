import os
import random
import datetime

import discord

from discord.ext import commands
from easypydb import DB
from dotenv import load_dotenv


TOKENDB = os.getenv('TOKENDB')
database = DB("MoneyDB", TOKENDB)


# Define all Basic commands
class Basic(commands.Cog):
    """fft, roll, add, work, balance"""
    def __init__(self, bot):
        self.bot = bot

# Commands that are just for fun.
    @commands.command(name='fft', help='Responds with a random quote from Final Fantasy Tactics')
    async def fft_command(self, ctx):
        #fft_quotes = ['Names don\'t matter. What\'s important is how you live your life.', 'A \'heretic\' coming to church... pretty bold...', 'Ignorance itself is a crime!']
        with open('fft_quotes.txt', 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            emb = discord.Embed(
                title='FFT Quote',
                description=random.choice(lines),
                color=discord.Colour.green()
            )
            await ctx.send(embed=emb)

    @commands.command(name='roll', help='Rolls dice in NdN format')
    async def roll_command(self, ctx, dice: str):
        # Rolls a dice in NdN format.
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!', delete_after=10)
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(name='add', help='Adds two numbers together.')
    async def add(self, ctx, left: int, right: int):
        await ctx.send(left + right)

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
            sec = error.retry_after
            conv = datetime.timedelta(seconds = int(sec))
            em = discord.Embed(title=f'Hold yer horses, kid.',description=f'Try again in {conv}s', color=discord.Colour.green())
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
