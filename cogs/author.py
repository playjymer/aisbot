import disnake
from disnake.ext import commands

class Author(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Узнать автора бота")
    async def author(self, ctx):
        await ctx.send("Бота создал любимый Грогу🖤")


def setup(bot: commands.Bot):
    bot.add_cog(Author(bot))