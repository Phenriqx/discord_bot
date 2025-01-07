import discord
from discord.ext import commands
import json


class RolesAutomation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('automation_roles.py is ready')
        
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('cogs/json/autorole.json', 'r') as f:
            auto_role = json.load(f)
        
        join_role = discord.utils.get(member.guild.roles, name=auto_role[str(member.guild.id)])
        await member.add_roles(join_role)
        

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def joinrole(self, ctx, role: discord.Role):
        with open('cogs/json/autorole.json', 'r') as f:
            auto_role = json.load(f)
            
        auto_role[str(ctx.guild.id)] = str(role.name)
        
        with open('cogs/json/autorole.json', 'w') as f:
            json.dump(auto_role, f, indent=4)
            
        conf_embed = discord.Embed(color=discord.Color.green())
        conf_embed.add_field(name='Success!', value=f'The automatic role for this server has been set to {role.mention}')
        conf_embed.set_footer(text=f'Action taken by {ctx.author.name}.')
        
        await ctx.send(embed = conf_embed)
            
            
    # Command that checks the roles assigned to a given player on the server 
    @commands.command('check-roles')
    async def check_roles(self, ctx, *, member: discord.Member):
        roles = [role.name for role in member.roles]
            
        if len(roles) == 1:
            await ctx.send(f'This user currently does not have any roles!')
        else:
            await ctx.send(f'The member {member.name} has the following roles: {roles}')
  
  
    # Creates a role with a given name    
    @commands.command('create-role')
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, role: str):
        guild = ctx.guild
        await guild.create_role(name=role, 
                                color=discord.Color(0xd9e906),
                                mentionable=True)
        await ctx.send(f'The role "{role}" was created by {ctx.message.author}.')
        
        
    # Deletes a given role   
    @commands.command('delete-role')
    @commands.has_permissions(manage_roles=True)
    async def delete_role(self, ctx, *, role: discord.Role):
        role = discord.utils.get(ctx.message.guild.roles, name=f"{role}")
        await role.delete()
        await ctx.send(f"[{role}] Has been deleted!")
        
    
    # Add a given role to a specified player
    @commands.command('add-role')
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, role_name: str, member: discord.Member, *, reason: str):
        role = discord.utils.get(ctx.message.guild.roles, name=f"{role_name}")
        if not role:
            await ctx.send('This role does not exist!')
        else:
            await member.add_roles(role_name)
            await ctx.send(f"""The role [{role_name}] has been assigned to {member.name.capitalize()}!\n
                       Reason: {reason}.""") 
        
        
    # Remove a given role from a specified player    
    @commands.command('remove-role')
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, role: discord.Role, member: discord.Member):
        await member.remove_roles(role)
        await ctx.send(f'The role [{role}] has been taken away from {member.name}!')
    
        
async def setup(client):
    await client.add_cog(RolesAutomation(client))