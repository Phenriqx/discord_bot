import discord
from discord.ext import commands
import random


class RolesAutomation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('automation_roles.py is ready')
        
    # Command that displays all the roles on the server    
    @commands.command('fetch-roles')
    async def fetch_roles(self, ctx):
        guild = ctx.guild
        roles = [role.name for role in guild.roles]
        print(roles)
        await ctx.send(f'List of all the roles in the server: {roles}')
            
            
    # Command that checks the roles assigned to a given player on the server 
    @commands.command('check-roles')
    async def check_roles(self, ctx, *, member: discord.Member):
        # if member not in ctx.guild.members:
        #     await ctx.send('This player is currently not in the server.')
        
        roles = [role.name for role in member.roles]
            
        if len(roles) == 1:
            await ctx.send(f'This user currently does not have any roles!')
        else:
            await ctx.send(f'The member {member.name} has the following roles: {roles}')
  
  
    # Creates a role with a given name    
    @commands.command('create-role')
    @commands.has_role('admin')
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, role: str):
        guild = ctx.guild
        await guild.create_role(name=role, 
                                color=discord.Color(0xd9e906),
                                mentionable=True)
        await ctx.send(f'The role "{role}" was created by {ctx.message.author}.')
        
        
    # Deletes a given role   
    @commands.command('delete-role')
    @commands.has_role('admin')
    @commands.has_permissions(manage_roles=True)
    async def delete_role(self, ctx, *, role: discord.Role):
        role = discord.utils.get(ctx.message.guild.roles, name=f"{role}")
        await role.delete()
        await ctx.send(f"[{role}] Has been deleted!")
        
        
    @commands.command('add-role')
    @commands.has_role('admin')
    async def add_role(self, ctx, role: discord.Role, member: discord.Member):
        pass 
    
        
async def setup(client):
    await client.add_cog(RolesAutomation(client))