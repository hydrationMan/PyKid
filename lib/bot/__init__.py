# Modules to Import
import discord
from asyncio import sleep
from glob import glob
from apscheduler.triggers.cron import CronTrigger
from discord import Intents
from discord.ext import commands
from datetime import datetime
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord.ext.commands import Cog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..db import db

# PREFIX, will respond to anything valid command following Prefix.
# OWNER_IDS, If User has the ID, bot will respond
# COGS, specify where to load cogs (additional commands) from

PREFIX = "+"
OWNER_IDS = [344291973030608897]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]

# Once Cog is Ready, print "Cog Ready"
class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog)])


# Some Configuration
class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()
        self.ready = False

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())
    
    # Once cog is loaded, print "cog loaded"
    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(F" {cog} cog loaded")

        # Once all cogs have finished loading, print "Setup Complete"
        print("Setup Complete")

    # obtain Version and print "Running Setup...", begin setup
    def run(self, version):
        self.VERSION = version
        print("Running Setup...")
        self.setup()

        # Find file named 'token.0' and open in Read Only Mode with UTF-8 Encoding as 'tf'
        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        # print "Booting...", apply loaded token.0 and begin connection attempt
        print("Booting...")
        super().run(self.TOKEN, reconnect=True)

    # I'll get back to this one
    async def print_message(self):
        await self.stdout.send("You ever just timed notifications?")


    # On successful connection to API, print "Boot Complete, Connected"
    async def on_connect(self):
        print("Boot Complete, Connected")

    # On disconnection from API, print "Disconnected"
    async def on_disconnect(self):
        print("Disconnected")

    # On Error, print "An Error Ocuured" to console and connected discord guild(server)
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("An Error Ocurred")

        await self.stdout.send("An Error Ocurred")

        raise

    # On Command Not Found, print "An Error Ocurred" to console
    async def on_command_error(self, ctx, exec):
        if isinstance(exc, CommandNotFound):
            await s.send("An Error Ocurred")

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    # On Ready, run this, print "We Ready". If not Ready, print "Bot Reconnected"
    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(633873140618887169)
            self.stdout = self.get_channel(633873140618887171)
            # self.scheduler.add_job(self.print_message, CronTrigger(second="0,15,30,45"))
            # self.scheduler.start()
            # await self.stdout.send("Ready.")

            # channel = self.get_channel(633873140618887171)

            # embed = discord.Embed(title="PyKid", description="Bootup Status",
            #                     color=0xBB33FF, timestamp=datetime.utcnow())
            # fields = [("State?", "Connected", True),
            #           ("Revision?", "0.0.7", True),
            #           ("Functionality apart from being Online?", "None", False)]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            #     embed.set_author(name="PyKid", icon_url=self.guild.icon_url)
            #     embed.set_footer(text="Peck Neck")
            # await channel.send(embed=embed)
            
            # On none or not all Cogs Ready, sleep for 0.5
            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("We Ready")

        else:
            print("Bot Reconnected")
            

    # On prefix & command, Ignore
    async def on_message(self, message):
        pass

bot = Bot()

    
