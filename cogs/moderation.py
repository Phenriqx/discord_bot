import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('moderation.py is ready')
        
    # Command to clear the amount of messages inputted by the user
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.has_role('admin')
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        await ctx.send(f'{count} message(s) deleted!')
     
        
    # Command to kick a member due to a reason specified by the author
    @commands.command()
    @commands.has_role('admin')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member_name: discord.Member, *, reason):
        await ctx.guild.kick(member_name)
        
        conf_embed = discord.Embed(title='Success!', color=discord.Color.green())
        conf_embed.add_field(name='Kicked:', value=f'{member_name.mention} has been kicked from the server by {ctx.author.mention}.', inline=False)
        conf_embed.add_field(name='Reason', value=reason, inline=False)
        
        await ctx.send(embed = conf_embed)
        
        
    # Command to ban a member due to a reason specified by the author
    @commands.command()
    @commands.has_role('admin')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member_name: discord.Member, *, reason):
        await ctx.guild.ban(member_name)
        
        conf_embed = discord.Embed(title='Success!', color=discord.Color.green())
        conf_embed.add_field(name='Banned:', value=f'{member_name.mention} has been banned from the server by {ctx.author.mention}.', inline=False)
        conf_embed.add_field(name='Reason', value=reason, inline=False)
        
        await ctx.send(embed = conf_embed) 
        

    # Command to unban an ex-member
    @commands.command(name='unban')
    @commands.has_role('admin')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)   
        await ctx.guild.unban(user)
        
        conf_embed = discord.Embed(title='Success!', color=discord.Color.green())
        conf_embed.add_field(name='Unbanned:', value=f'<@{userId}> has been unbanned from the server by {ctx.author.mention}.', inline=False)   
        
        await ctx.send(embed = conf_embed)    
            
            
async def setup(client):
    await client.add_cog(Moderation(client))