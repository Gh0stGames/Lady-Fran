import os
import random
import datetime
import json

import discord

from discord.ext import commands
from easypydb import DB
from dotenv import load_dotenv

# Get database token from .env file
TOKENDB = os.getenv('TOKENDB')
database = DB("MoneyDB", TOKENDB)


# Define all Basic commands
class Fun(commands.Cog):
    """fft, roll, add, work, balance"""
    def __init__(self, bot):
        self.bot = bot

# Commands that are just for fun.
    @commands.command(
        name='fft',
        help='Responds with a random quote from Final Fantasy Tactics'
    )
    async def _fft(self, ctx):
        quotes = _get_quotes()
        await ctx.send(quotes)

    async def _get_quotes(self):
        with open('fft_quotes.txt', 'r') as quotes:
            quote = file.readlines(self)
        return quote

    @commands.command(
        name='roll',
        help='Rolls dice in NdN format'
    )
    async def _roll(self, ctx, dice: str):
        # Rolls a dice in NdN format.
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!', delete_after=10)
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(
        name='add',
        help='Adds two numbers together.'
    )
    async def _add(self, ctx, left: int, right: int):
        await ctx.send(left + right)

    @commands.command(
        name='coinflip'
    )
    async def _coinflip(self, ctx):
        result = random.randint(0, 1)
        if result == 0:
            emb = discord.Embed(title=f'Coinflip',description=f'{ctx.message.author.mention} The coin landed on... Tails!',color=discord.Colour.green())
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title=f'Coinflip',description=f'{ctx.message.author.mention} The coin landed on... Heads!',color=discord.Colour.green())
            await ctx.send(embed=emb)
        await ctx.message.delete()

    @commands.command(
        name='lotto'
    )
    async def _lottery(self, ctx):
        final = []
        for i in range(3):
            a = random.choice(['X','O','Q'])

            final.append(a)
        emb = discord.Embed(title=f'Lottery',description=str(final),color=discord.Colour.green())
        await ctx.send(embed=emb, delete_after=15)
        if final[0] == final[1] == final[2]:
            emb = discord.Embed(title='Winner, winner, chicken dinner!',description=f'Congrats, {ctx.author.mention}! You won!',color=discord.Colour.green())
            await ctx.send(embed=emb, delete_after=15)
        else:
            emb = discord.Embed(title=f'What a loser...',description=f'You get... NOTHING!!! YOU LOSE!! GOOD DAY, SIR!!!',color=discord.Colour.green())
            await ctx.send(embed=emb, delete_after=15)
        await ctx.message.delete()

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
    bot.add_cog(Fun(bot))
