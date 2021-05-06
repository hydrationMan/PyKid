import os
import time
import random
import discord
from ..db import db 
from glob import glob
from asyncio import sleep
from aiohttp import request
from discord import Intents
from datetime import datetime
from discord import Embed, File 
from discord.ext.commands import Context
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord.errors import HTTPException, Forbidden
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)


PREFIX = "+"
OWNER_IDS = [344291973030608897]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)
CHANNEL_NAME = ""
STATUS = ["Now with a working mute command", "Obtaining The Time Pieces", "Do +help for a list of commands"]
class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" {cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")
                
    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO exp (UserID) VALUES (?)",
                     ((member.id,) for guild in self.guilds for member in guild.members if not member.bot))

        to_remove = []
        stored_members = db.column("SELECT UserID from exp")
        for id_ in stored_members:
            #print(self.guild.get_member(id_))
            if not self.guild.get_member(id_):
                to_remove.append(id_)

        db.multiexec("DELETE FROM exp WHERE UserID = ?",
                     ((id_,) for id_ in to_remove))


        db.commit

    def run(self, version):
        self.VERSION = version
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running Bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot Connected")

    async def on_disconnect(self):
        print("Bot Disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Error.")

        await self.stdout.send(exc)
        print(exc)
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Command Not Found, or im dying.")
            await self.stdout.send(exc)
            print(exc)

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("I need an additional argument you spoon")
            await ctx.send(exc)
            print(exc)

        elif isinstance(exc.original, HTTPException):
            await ctx.send("Cannot comply, The user you're trying to ban may have administrative permissions. Or something is terribly wrong")
            await ctx.send(exc)
            print(exc)

        elif isinstance(exc.original, Forbidden):
            await ctx.send("Cannot comply, Forbidden request.")
            await ctx.send(exc)
            print(exc)

        elif hasattr(exc, "original"):
            raise exc.original
        
        else:
            raise exc


    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(633873140618887169)
            self.stdout = self.get_channel(828466661622415380)
            #self.scheduler.start()
            #self.update_db()

            # Embed
            #await channel.send("Online")

            #embed = discord.Embed(title="Haha", description="Stole your embed colour, Liam!",
            #                      colour=0xFAFC00, timestamp=datetime.utcnow())
            #fields = [("Color:", "0xFAFC00", True),
            #          ("Too Smart", "No one can possibly match me", True),
            #          ("Not even a chance", "Nope, not one", False)]
            #for name, value, inline in fields:
            #    embed.add_field(name=name, value=value, inline=inline)
            #embed.set_author(name="PyKid", icon_url=self.guild.icon_url)
            #embed.set_footer(text="Get Rekt")
            #embed.set_thumbnail(url=self.guild.icon_url)
            #embed.set_image(url=self.guild.icon_url)
            #await channel.send(embed=embed)
            
            # Boop
            #await channel.send(file=discord.File(".data/assets/boop.gif"))
            self.ready = True
            await self.stdout.send("Online")
            await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="you stupid fucks"))
            print("Bot Ready")
            

        else:
            print("Bot Reconnected")


    async def on_message(self, message):
            if not message.author.bot:
                await self.process_commands(message)
            if str(message.channel) != CHANNEL_NAME:
                return
            if not message.content:
                return

    
            
        

bot = Bot()