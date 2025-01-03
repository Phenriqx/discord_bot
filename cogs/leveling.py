import discord
from discord.ext import commands
import sqlite3
import math
import random


class LevelSys(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('leveling.py is ready')
        

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        con = sqlite3.connect('./cogs/levels.db')
        cursor = con.cursor()
        guild_id = message.guild.id
        user_id = message.author.id
        
        cursor.execute('SELECT * FROM USERS WHERE guild_id = ? AND user_id = ?', (guild_id, user_id))
        result = cursor.fetchone()
        
        if result == None:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            cursor.execute('INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) VALUES (?, ?, ?, ?, ?)', (guild_id, user_id, cur_level, xp, level_up_xp))
        else:
            cur_level = result[2]
            xp = result[3]
            level_up_xp = result[4]
            
            xp += random.randint(2, 20)
            
        if xp >= level_up_xp:
            cur_level += 1
            new_level_up_xp = math.ceil(50 * cur_level ** 2 + 200 * cur_level + 50)
            
            await message.channel.send(f'{message.author.mention} has leveled up to level {cur_level}!')
            cursor.execute('UPDATE Users SET level = ?, xp = ?, level_up_xp = ? WHERE guild_id = ? AND user_id = ?', (cur_level, xp, new_level_up_xp, guild_id, user_id))
            
        cursor.execute('UPDATE Users SET xp = ? WHERE guild_id = ? AND user_id = ?', (xp, guild_id, user_id))
        con.commit()
        con.close()
        
    @commands.command()
    async def level(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
            
        member_id = member.id
        guild_id = ctx.guild.id
        
        con = sqlite3.connect('./cogs/levels.db')
        cursor = con.cursor()
        cursor.execute('SELECT * FROM Users WHERE guild_id = ? AND user_id = ?', (guild_id, member_id))
        result = cursor.fetchone()
        
        if result is None:
            await ctx.send(f'{member.name} does not have a level.')
        else:
            level = result[2]
            xp = result[3]
            level_up_xp = result[4]
            await ctx.send(f"""Level Statistics for {member.name}\n
                           - Level: {level}\n
                           - Xp: {xp}\n
                           - Xp to next level: {level_up_xp}""")
            
        con.close()
        
async def setup(client):
    await client.add_cog(LevelSys(client))