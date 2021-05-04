import discord
from discord.ext.commands import Cog
from discord.ext.commands import command 

class Egg(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(brief="Gives you an Egg") #Optional: "(name=*name*), (alias=*alias*)"
    async def egg(self, ctx):
        """Here, Egg"""
        await ctx.send(file=discord.File("data/assets/egg.jpg"))


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("egg")

def setup(bot):
    bot.add_cog(Egg(bot))
