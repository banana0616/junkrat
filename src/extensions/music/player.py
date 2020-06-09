from discord.ext import commands
import discord
import youtube_dl
import asyncio
from discord import utils
import sqlite3


class Player(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = sqlite3.connect('playlist.db')

    @commands.command(name="정크랫")
    async def 정크랫(self, ctx):
        await ctx.send('왜 불렀음?')

    @commands.command(name="아", aliases=["재생"])
    async def 아(self, ctx: commands.Context, *q:str):
        url = ' '.join(q)
        ytdl_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'./songs/{ctx.guild.id}/%(extractor)s-%(id)s.mp3'
        }
        ytdl = youtube_dl.YoutubeDL(ytdl_options)

        loop = asyncio.get_event_loop()

        if url.startswith('https://') or url.startswith('http://'):
            utype = 'url'
        else:
            utype = 'query'

        def fetch_video():
            if utype == 'url':
                return ytdl.extract_info(url)
            elif utype == 'query':
                return ytdl.extract_info(f"ytsearch:{url}")

        data = await loop.run_in_executor(None, lambda: fetch_video())

        if 'entries' in data:
            data = data['entries'][0]
        vc = self.get_voice_client(ctx)
        source = ytdl.prepare_filename(data)
        vc.play(source=discord.FFmpegPCMAudio(source=source))
        embed = discord.Embed(title="플레이중")
        embed.add_field(name="곡 정보", value=f"제목: {data.get('title')}")
        await ctx.send(embed=embed)

    @commands.command(name="stop", aliases=["정지"])
    async def stop(self, ctx: commands.context):
        self.get_voice_client(ctx).stop()

    @commands.command(name="플레이리스트", aliases=['playlist'])
    async def playlist(self, ctx: commands.Context):
        con = self.db
        con.execute(f'CREATE TABLE IF NOT EXISTS pl_{ctx.guild.id}(query varchar(255))')
        con.commit()
        await ctx.send('플레이리스트')

    def get_voice_client(self, ctx: commands.Context) -> discord.VoiceClient:
        return utils.get(self.bot.voice_clients, guild=ctx.guild)
