import os
import sys
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# def to_upper(argument):cl
#    return argument.upper()

#@bot.command()
#async def up(ctx, *, content: to_upper):
#    await ctx.send(content)




class JoinDistance:
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @classmethod
    async def convert(cls, ctx, argument):
        member = await commands.MemberConverter().convert(ctx, argument)
        return cls(member.joined_at, member.created_at)

    @property
    def delta(self):
        return self.joined - self.created


@bot.command()
async def delta(ctx, *, member: JoinDistance):
    is_new = member.delta.days < 100
    print(member.delta.days)
    if is_new:
        await ctx.send("Hey you're pretty new!")
    else:
        await ctx.send("Hm you're not so new.")
    

# Check connection between the bot and the guild
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    

# Displays a list of all members on the guild
@bot.command('members')
async def members_list(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    members = '\n - '.join([member.name for member in guild.members])
    
    await ctx.send(f'All guild members:\n - {members}')
        

# Command that simulates a player rolling a dice
@bot.command('roll_dice')
async def roll(ctx, number_of_dice: int, number_of_sides: int, ):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    
    await ctx.send(', '.join(dice))

# Command for creating a voice channel
@bot.command('create_voice_channel', help='Create a voice channel')
@commands.has_role('admin')
async def create_voice_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel and channel_name != None:
        await guild.create_voice_channel(channel_name)
        await ctx.send(f'Voice channel created as {channel_name} by {ctx.author}')
        

# Command for creating a text channel
@bot.command('create_text_channel', help='Create a text channel')
@commands.has_role('admin')
async def create_text_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel and channel_name != None:
        await guild.create_text_channel(channel_name)
        await ctx.send(f'Text channel created as {channel_name} by {ctx.author}')
        
        
# Command for deleting any channel
@bot.command(name='delete-channel', help='delete a channel with the specified name')
async def delete_channel(ctx, channel_name):
   guild = ctx.guild
   existing_channel = discord.utils.get(guild.channels, name=channel_name)
   
   if existing_channel is not None:
      await existing_channel.delete()
      await ctx.send(f'Channel {channel_name} deleted')
   else:
      await ctx.send(f'No channel named "{channel_name}" was found')


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


bot.run(TOKEN)