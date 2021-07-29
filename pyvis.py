import discord
import os
from cogs.finance import Finance
from cogs.python import Python
from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import DefaultMenu, PrettyHelp

# load environment variables from .env file
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_NAME = os.getenv('DISCORD_GUILD_NAME')
PREFIX = "!"

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == DISCORD_GUILD_NAME, bot.guilds)
    if guild:
        print(
            f'{bot.user} is connected to the following guild:\n',
            f'{guild.name}(id: {guild.id})'
        )   

@bot.event 
async def on_member_join(member):
    pass # TODO

@bot.event
async def on_message(message):
    # avoid bot self trigger
    if message.author == bot.user:
        return

    # repsond with command prefix
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        await message.channel.send(f"**My prefix in this server is:** `{PREFIX}`")

    # allow cogs to handle messages too
    await bot.process_commands(message)

# override default help command
menu = DefaultMenu('◀️', '▶️', '❌')
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green()) 

# commands by category a.k.a. cogs
bot.add_cog(Python())
bot.add_cog(Finance())

# start up bot
bot.run(DISCORD_BOT_TOKEN)