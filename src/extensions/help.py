from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.command(name="도움말", aliases=["help"])
    async def help(self, ctx):
        embed = discord.Embed(title="도움말")
        embed.add_field(name="냠?", value="냠냠")
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))