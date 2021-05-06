import discord
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

class Ban(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} is fuckin outta here')
        print(f'{member} is fuckin outta here')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("ban")

# Setup Function, again discord documentation wisdom
def setup(bot):
    bot.add_cog(Ban(bot))
    