from discord.ext import commands
import random
import discord


class Basic(commands.Cog):
    """Contains all basic commands."""
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name='create-channel', help='Allows an admin to create a new text channel.')
    @commands.has_role('Admin')
    async def create_channel(self, ctx, channel_name='Test-Channel'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)

def setup(bot):
    bot.add_cog(Basic(bot))
