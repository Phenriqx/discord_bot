import discord
from discord.ext import commands


class ChannelControl(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('channel_control.py is ready')
        
    
    # Created a text channel
    @commands.command('create-text-channel')
    @commands.has_role('admin')
    async def create_text_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        if not existing_channel and channel_name != None:
            await guild.create_text_channel(channel_name)
            await ctx.send(f'Text channel created as {channel_name} by {ctx.author}')
                        

    # Creates a voice channel
    @commands.command('create-voice-channel')
    @commands.has_role('admin')
    async def create_voice_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        if not existing_channel and channel_name != None:
            await guild.create_voice_channel(channel_name)
            await ctx.send(f'Voice channel created as {channel_name} by {ctx.author}')


    # Deletes a channel
    @commands.command('delete-channel')
    @commands.has_role('admin')
    async def delete_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel != None:
            await existing_channel.delete()
            await ctx.send(f'Channel [{channel_name}] deleted!')
        else:
            await ctx.send(f'No channel named {channel_name} was found!')
    
    
async def setup(client):
    await client.add_cog(ChannelControl(client))