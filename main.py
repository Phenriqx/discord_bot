import os
import sys
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


@bot.command(name='99')
async def on_message(ctx):
    # testing the command function
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
    
async def on_error(event, *args, **kwargs):
    with open('err.log') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}/n')
        else:
            raise sys.exc_info()


bot.run(TOKEN)