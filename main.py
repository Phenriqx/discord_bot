import os
import sys
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# Add an activity to the bot on the discord interface
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game('Discord'))


# Check connection between the bot and the guild
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    change_status.start()

    
# Load cogs folder with the command files
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)
        

# Welcomes new members to the server
@bot.event
async def on_member_join(member, ctx):
    await member.create_dm()
    await member.dm_channel_send(
        f'Welcome {member.name}'
    )
    await member.channel.send(f'Hello, {member.name}. Welcome to the server')        
    

# Events that handle certain errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}/n')
        else:
            raise sys.exc_info()
        
asyncio.run(main())