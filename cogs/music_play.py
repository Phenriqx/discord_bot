import discord
import yt_dlp
import asyncio
from discord.ext import commands
import urllib.parse, urllib.request, re


class Music(commands.Cog):
    queues = {}
    voice_clients = {}
    youtube_base_url = 'https://www.youtube.com/'
    youtube_results_url = youtube_base_url + 'results?'
    youtube_watch_url = youtube_base_url + 'watch?v='
    yt_dl_options = {'format': 'bestaudio/best'}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
    
    ffmpeg_options = {'options': '-vn'}
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('music.py is ready')
        
    
    async def play_next(self, ctx):
        if self.queues[ctx.guild.id] != {}:
            link = self.queues[ctx.guild.id].pop(0)
            await self.play(ctx, link=link)
    
            
    @commands.command(name='play')
    async def play(self, ctx, *, link):
        try:
            voice_client = await ctx.author.voice.channel.connect()
            self.voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)
            
        try:
            if self.youtube_base_url not in link:
                query_str = urllib.parse.urlencode({
                    'search_query': link,
                })
                
                content = urllib.request.urlopen(self.youtube_results_url + query_str)
                search_result = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                
                link = self.youtube_watch_url + search_result[0]
                
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(link, download=False))       
            
            song = data['url']
            player = discord.FFmpegPCMAudio(song, **self.ffmpeg_options)
            
            self.voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.client.loop))
        except Exception as e:
            print(e)
            
    
    @commands.command(name='clear-queue')
    async def clear_queue(self, ctx):
        if ctx.guild.id in self.queues:
            self.queues[ctx.guild.id].clear()
            await ctx.send('Cleared the queue!')
        else:
            await ctx.send('Queue is empty.')
                
    
    @commands.command(name='pause')
    async def pause(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(e)
            
            
    @commands.command(name='resume')
    async def resume(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(e)
            
    
    @commands.command(name='stop')
    async def stop(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].stop()
            await self.voice_clients[ctx.guild.id].disconnect()
            del self.voice_clients[ctx.guild.id]
            await ctx.send('Exiting channel!')
        except Exception as e:
            print(e)
            
                
    @commands.command(name='queue')
    async def queue(self, ctx, *, url):
        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []
        self.queues[ctx.guild.id].append(url)
        await ctx.send('Added to the queue!')
                
        
async def setup(client):
    await client.add_cog(Music(client))