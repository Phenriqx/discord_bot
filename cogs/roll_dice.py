import discord
from discord.ext import commands
import random


class RollDice(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('roll_dice.py is ready')
        
    @commands.command('roll-dice')
    async def roll_dice(self, ctx, number_of_sides:int, number_of_dice:int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        
        await ctx.send(', '.join(dice))
        

async def setup(client):
    await client.add_cog(RollDice(client))