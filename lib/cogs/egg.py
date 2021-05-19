# Imports
import discord
from discord.ext.commands import Cog
from discord.ext.commands import command 

# Specify cog name when loaded?
class Egg(Cog):
    def __init__(self, bot):
        self.bot = bot

# The command Itself, sends a phot of Egg when called
    @command(name="egg", brief="Gives you an Egg") #Optional: "(name=*name*), (alias=*alias*)"
    async def egg(self, ctx):
        """Here, Egg"""
        await ctx.send(file=discord.File("data/assets/egg.jpg"))


# Code to interact with cog loader
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("egg")

# Setup
def setup(bot):
    bot.add_cog(Egg(bot))
