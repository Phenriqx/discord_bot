import discord
from discord.ext import commands


class MembersList(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('members_list.py is ready')
        
    @commands.command('members', help='Displays a list of all members on the server!')
    async def get_members(self, ctx):
        guild = ctx.guild
        members = '\n - '.join([member.name for member in guild.members])
        
        await ctx.send(f'All guild members:\n - {members}')
        
        
async def setup(client):
    await client.add_cog(MembersList(client))