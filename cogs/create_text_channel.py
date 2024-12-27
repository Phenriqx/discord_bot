import discord
from discord.ext import commands


class CreateTextChannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('create_text_channel.py is ready')
        
    @commands.command('create-text-channel')
    @commands.has_role('admin')
    async def create_text_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        if not existing_channel and channel_name != None:
            await guild.create_text_channel(channel_name)
            await ctx.send(f'Text channel created as {channel_name} by {ctx.author}')
            
            
async def setup(client):
    await client.add_cog(CreateTextChannel(client))