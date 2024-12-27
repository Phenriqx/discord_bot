import discord
from discord.ext import commands


class CreateVoiceChannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('create_voice_channel.py is ready')
        
    @commands.command('create-voice-channel')
    @commands.has_role('admin')
    async def create_voice_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        if not existing_channel and channel_name != None:
            await guild.create_voice_channel(channel_name)
            await ctx.send(f'Voice channel created as {channel_name} by {ctx.author}')
            

async def setup(client):
    await client.add_cog(CreateVoiceChannel(client))