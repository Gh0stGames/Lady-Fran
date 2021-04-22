# Currently not in use, will try to make it work as a cog file later.
import random
import os

import discord

from discord.ext import commands


class Destroy(commands.Cog):
    """Destroy command"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name = 'destroy',
        brief = 'Destroys a user',
        help = 'Prints out a random boss "final move" quote directed at a user.'
    )
    async def destroy(self, ctx, user: discord.User):
        quote = [(f"MISFORTUNE HANGS HEAVY ON A HEAD ONCE HELD HIGH.\nSUCH IS POOR COVER FOR WHEN  THE HEAVENS "
        f"FALL!\nCrush Helm on {user.mention}!"),
        (f"To the current of life we succumb, its judgement swift and final!\nIts bite as cold as "
        f"steel.\nJudgement Blade on {user.mention}!"),
        f"The hearts of men are black with corruption, and must needs be cleansed!\nCleansing Strike on {user.mention}!",
        (f"Seven shadows cast, seven fates fortold. Yet at the end of the broken path\nlies death, and death "
        f"alone!\nNorthswain's Strike on {user.mention}!"),
        (f"I call out the the skies and tremble\nas the brilliance of a thousand bolts\nblinds mine enemies and "
        f"tears their flesh asunder!\nHallowed Bolt on {user.mention}!"),
        (f"They who dwell aloft have spoken.\nLet their words echo in your empty soul!\nRuination is "
        f"come!\nDivine Ruination on {user.mention}!"),
        (f"Even the strongest of shields cannot defend the weakest of wills.\nA moment's hesitation beckons a "
        f"lifetime of pain!\nCrush Armor on {user.mention}!"),
        (f"Honed is the blade that severs the villain's head.\nEndless is the path that leads him from "
        f"Hell.\nCrush Weapon on {user.mention}!"),
        (f"Hark!\nThe screams of ruin rise above the storm's discord.\nShudder not in her endless cold!\nCrush "
        f"Accessory on {user.mention}"),
        (f"To live by the sword is to die by the sword!\nThere is time enough for regret in the flames of Hell! "
        f"Duskblade on {user.mention}!"),
        (f"Open your eyes to the darkness,\nand drown in its loveless embrace.\nThe gods will not be "
        f"watching.\nShadowblade on {user.mention}!"),
        (f"Bright light, shine down on bloody impurity!\nHoly on {user.mention}!"),
        (f"Smoldering flames far below\npunish the wicked!\nFire 4 on {user.mention}!"),
        (f"Effortless water\nbreak your silence! Attack!\nIce 4 on {user.mention}!"),
        (f"Angry spirits of the world, strike now!\nThunder 4 on {user.mention}!"),
        ]
        response = random.choice(quote)
        emb = discord.Embed(title='Get Destroyed, kid!',description=response,color=discord.Colour.green())
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Destroy(bot))
