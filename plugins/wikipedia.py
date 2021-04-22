# Cog file for the wikipedia Commands
import wikipedia
import discord

from discord.ext import commands


class Wikipedia(commands.Cog):
    """wiki, wikisearch"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='wiki',help='Search the Wikipedia database.')
    async def _wikipedia(self, ctx, *, question):
        search = wikipedia.summary(question, sentences=3)
        emb = discord.Embed(title=f'Search Results',description=search,color=discord.Colour.green())
        await ctx.message.delete()
        await ctx.send(embed=emb, delete_after=60)

    @commands.command(name='wikisearch',help='Find a list of related search terms.')
    async def _wikipedia_search(self, ctx, *, question):
        search = wikipedia.search(question, results=10)
        emb = discord.Embed(title=f'Search Results',description=search,color=discord.Colour.green())
        await ctx.message.delete()
        await ctx.send(embed=emb, delete_after=30)


def setup(bot):
    bot.add_cog(Wikipedia(bot))
