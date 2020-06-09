from discord.ext import commands
import discord
import asyncio

class ClearCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.command(name="청소", aliases=['clear'])
    async def clear(self, ctx:commands.Context, cnt:str = None):
        if not cnt:
            await ctx.send('사용법: -청소 <청소할 채팅 수>')
        else:
            if cnt.isnumeric():
                lst = await ctx.message.channel.history(limit=int(cnt)).flatten()
                amount = len(lst)
                while amount > 99:
                    await ctx.message.channel.delete_messages(lst[0:99])
                    for i in range(0, 99):
                        lst.remove(i)
                await ctx.message.channel.delete_messages(lst)
                embed = discord.Embed(title=f"메시지 {amount}개가 삭제되었습니다.")
                await ctx.send(embed=embed)
            else:
                await ctx.send('청소할 개수가 문자입니다')
    async def cog_check(self, ctx:commands.Context):
        if not ctx.guild:
            return False
        if not ctx.author.guild_permissions.administrator:
            return await self.bot.is_owner(ctx.author)
        return True