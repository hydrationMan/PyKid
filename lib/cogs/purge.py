# Imports (duh)
import discord
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

# I dont really know myself but discord documentation says this makes cogs work
class Purge(Cog):
    def __init__(self, bot):
        self.bot = bot 

# Actual Commmand(s), look after the 'async def' for the command name.
    @command(pass_context=True, brief="run help mod for moderation help")
    async def purge(self, ctx,amount=2):
        """Again, Purge x Amount of Messages"""
        await ctx.channel.purge(limit = amount)

# Tell the wacky auto cog loader thing that this cog in fact, exists.
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("purge")

# Setup Function, again discord documentation wisdom
def setup(bot):
    bot.add_cog(Purge(bot))