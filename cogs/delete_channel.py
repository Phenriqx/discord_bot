import discord
from discord.ext import commands


class DeleteChannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('delete_channel.py is ready')
        
    @commands.command('delete-channel')
    @commands.has_role('admin')
    async def delete_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel != None:
            await existing_channel.delete()
            await ctx.send(f'Channel {channel_name} deleted!')
        else:
            await ctx.send(f'No channel named {channel_name} was found!')
            

async def setup(client):
    await client.add_cog(DeleteChannel(client))