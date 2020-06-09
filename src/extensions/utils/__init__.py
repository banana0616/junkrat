from discord.ext import commands
from .clear import ClearCommand

def setup(bot: commands.Bot):
    bot.add_cog(ClearCommand(bot))