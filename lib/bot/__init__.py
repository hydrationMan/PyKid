#Ze imports

#Not mine with just a few changes
#Copyright (c) 2020, Carberra Tutorials
#All rights reserved.
import os
import time
import random
import discord
import logging
import asyncio

from discord.ext.commands.core import command
from ..db import db 
from glob import glob
from asyncio import sleep
from aiohttp import request
from discord.ext import tasks
from discord import Intents
from datetime import datetime
from discord import Embed, File 
from discord.ext.commands import Context
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord.errors import HTTPException, Forbidden
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)

# Set level of verbose information printed to console (e.g: Errors)
logging.basicConfig(level=logging.INFO)

PREFIX = "+" # Bot command prefix (e.g: +help)
OWNER_IDS = [344291973030608897] # Specify bot "Owner" UserID, in this case mine. Dunno what purpose this serves but it makes things happier 
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")] # Automatic detection and loading of files(cogs) from "./lib/cogs" ending in ".py"
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument) # Bot will not terminate upon a CommandNotFound or BadArgument error
CHANNEL_NAME = "" # Optional specified channel name
STATUSES = ["Now with a working mute command", "Obtaining The Time Pieces", "Do +help for a list of commands"] # List of "watching, playing, etc." Statuses for the Bot, Currently unused.

# Something important to Ready cogs
class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

# Code to print list of "Ready" cogs
	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" {cog} cog ready")

# I have uh, forgotten what this does, all i know is that its neccecary
	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

# Defining of Bot, imported as BotBase, Bot Prefix, Ready status, optional guild(server) specification and scheduler specification, technically deprecated now.
class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        #db.autosave(self.scheduler) # Now deprecated database autosave.
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

# Cog config/setup whatever you wanna call it, actual code to LOAD cogs and print which cogs it has loaded
    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

# Actual setup of Bot, prepating to run
    def run(self, version):
        self.VERSION = version
        self.setup()

# Grab and read bot authentication token from token.0 with encoding utf-8
        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

# Start the actual bot.
        print("Running Bot...")
        super().run(self.TOKEN, reconnect=True)

# Print upon successful authentication/login and connection to discord
    async def on_connect(self):
        print("Bot Connected")

# Print upon Unexpected(or expected) Disconnection from Discord, commonly caused by wifi issues or the discord API or even discord as a whole being down
    async def on_disconnect(self):
        print("Bot Disconnected")

# Error Handling, upon command error, print "Error." to a dedicated log channel and print the actual exception to console, then raise the exception, causing termination
    async def on_error(exc, self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Error.")

        print(exc)
        raise exc

# If a command can not be found (E.G: Typo in command), Print "Command Not Found, or im dying" to the channel the "nonexistant" command was mentioned in, print exception to channel and console
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Command Not Found, or im dying.")
            await self.stdout.send(exc)
            print(exc)

# If command requires an argument, and it can not be found or is genuinely not specified by command mentioner. Print "I need an additional argument you spoon", print exception to channel and console
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("I need an additional argument you spoon")
            await ctx.send(exc)
            print(exc)

# If an HTTP Exception occurs(Of any type). Print (message seen below), Print exception to channel and console 
        elif isinstance(exc.original, HTTPException):
            await ctx.send("Cannot comply, You may not have administrative permissions. If you're trying to ban/kick someone, they probably have permissions higher than I. Or something is terribly wrong")
            await ctx.send(exc)
            print(exc)

# If a Forbidden Exception occurs(discord broke probably, or the bot got banned by discord), print message and log to channel and console
        elif isinstance(exc.original, Forbidden):
            await ctx.send("Cannot comply, Request denied by discord.")
            await ctx.send(exc)
            print(exc)

# Terminate upon an exception occuring, i think
        elif hasattr(exc, "original"):
            raise exc.original
        
        else:
            raise exc

# Code to execute once bot reaches "Ready" Status. Specified GuildID, Log Channel ID and Deprecated Embed Test (Any code in here will run as soon as the bot has finished booting)
    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(633873140618887169)
            self.stdout = self.get_channel(828466661622415380)

#Confirmation of bot reaching ready status, Specify user status(e.g playing x, watching x, streaming x, listening to x.) by Changing the end of discord.ActivityType.x Appropriately, specify what bot is watching/streaming/listening/playing
            self.ready = True
            await self.stdout.send("Online")
            #await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            print("Bot Ready")
            
# If a disconnection occurs and can successfully reconnect to Discord after, print "Bot Reconnected"
        else:
            print("Bot Reconnected")


# Ignore commands from users that are bots, Some multi server support code that i dont know how it really works
    async def on_message(self, message):
        if not message.author.bot:
                 await self.process_commands(message)
                 if str(message.channel) != CHANNEL_NAME:
                     return
                 if not message.content:
                     return
    


bot = Bot()

