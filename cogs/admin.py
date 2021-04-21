import discord

from discord.ext import commands


class Admin(commands.Cog):
    """create-channel, clear"""
    def __init__(self, bot):
        self.bot = bot


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
        await ctx.channel.purge(limit = 1)
        await ctx.channel.purge(limit = amount)
        emb = discord.Embed(title=f'Messages Cleared',description=f'{ctx.message.author.mention} has cleared {amount} previous lines of text.',color=discord.Colour.green())
        await ctx.send(embed=emb, delete_after=10)


def setup(bot):
    bot.add_cog(Admin(bot))
