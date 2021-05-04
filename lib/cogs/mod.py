import discord
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

class Purge(Cog):
    def __init__(self, bot):
        self.bot = bot 

    @command(pass_context=True, brief="run help mod for moderation help")
    async def purge(self, ctx,amount=2):
        """Again, Purge x Amount of Messages"""
        await ctx.channel.purge(limit = amount)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("purge")

def setup(bot):
    bot.add_cog(Purge(bot))