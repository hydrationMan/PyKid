import discord
from typing import Optional
from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command 

class Slap(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="slap", brief="slap someone") #Optional: "(name=*name*), (alias=*alias*)"
    async def slap(self, ctx, member: Member, *, reason: Optional[str] = "For reasons Unknown"):
        """Slap a bitch"""
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}.")

    

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Slap")

def setup(bot):
    bot.add_cog(Slap(bot))