import os
import sys
import discord
import asyncio
import discord.embeds
from dotenv import load_dotenv
from discord.ext import commands, tasks
import json


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
    

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.channels, name='welcome')
    
    welcome_embed = discord.Embed(title='Arrival logged', description='Welcome to the server!', color=discord.Color.green())
    
    welcome_embed.add_field(name='User:', value=f'{member.mention}', inline=False)
    await welcome_channel.send(embed = welcome_embed)
    
@bot.event
async def on_member_remove(member):
    welcome_channel = discord.utils.get(member.guild.channels, name='welcome')
    
    welcome_embed = discord.Embed(title='Departure logged', description='This user left the server!', color=discord.Color.red())
    
    welcome_embed.add_field(name='User:', value=f'{member.mention}', inline=False)
    await welcome_channel.send(embed = welcome_embed)

    
# Load cogs folder with the command files
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)
        

@bot.event
async def on_guild_join(guild):
    with open('cogs/json/autorole.json', 'r') as f:
        auto_role = json.load(f)  
    auto_role[str[guild.id]] = None
    
    with open('cogs/json/autorole.json', 'w') as f:
        json.dump(auto_role, f, indent=4)
        
    
@bot.event
async def on_guild_remove(guild):
    with open('cogs/json/autorole.json', 'r') as f:
        auto_role = json.load(f)
        
    auto_role.pop(str(guild.id))
    
    with open('cogs/json/autorole.json', 'w') as f:
        json.dump(auto_role, f, indent=4)


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