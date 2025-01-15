import discord
import yt_dlp
import asyncio
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('music.py is ready')
        
    @commands.Cog.listener()
    async def on_message(self, message):
        voice_clients = {}
        yt_dl_options = {'format': 'bestaudio/best'}
        ytdl = yt_dlp.YoutubeDL(yt_dl_options)
        
        ffmpeg_options = {'options': '-vn'}
        
        if message.content.startswith('!play'):
            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except Exception as e:
                print(e)
                
            try:
                url = message.content.split()[1]
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))       
                
                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
                
                voice_clients[message.guild.id].play(player)
            except Exception as e:
                print(e)    
                
        
async def setup(client):
    await client.add_cog(Music(client))