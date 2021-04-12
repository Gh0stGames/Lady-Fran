# bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event # Client alert whenever new user joins the server
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event # Not working, fix later
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event # Prints out a random quote when a specific word is used
async def on_message(message):
    if message.author == client.user:
        return

    fft_quotes = [
        'Names don\'t matter. What\'s important is how you live your life.',
        'A \'heretic\' coming to church... pretty bold...',
        (
            'Ignorance itself is a crime!'
        ),
    ]

    if message.content == 'FFT!':
        response = random.choice(fft_quotes)
        await message.channel.send(response)

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
