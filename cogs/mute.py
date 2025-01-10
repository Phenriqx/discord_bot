import discord
from discord.ext import commands


class MuteSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('mute.py is ready')
        
    @commands.command(name='mute')
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member):
        guild = ctx.guild
        muted_role = guild.get_role(1327100323990470748)
        await member.add_roles(muted_role)
        await ctx.send(f'The member {member.name} has been muted!')
        

    @commands.command(name='unmute')
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.guild
        muted_role = guild.get_role(1327100323990470748)
        await member.remove_roles(muted_role)
        await ctx.send(f'The member {member.name} has been unmuted!')
                
                
async def setup(client):
    await client.add_cog(MuteSystem(client))