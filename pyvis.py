import discord
import os
import requests
import json
import random
from cogs.python import Python
from cogs.fun import Fun
from cogs.finance import Finance
from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import DefaultMenu, PrettyHelp

# load environment variables from .env file
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_NAME = os.getenv('DISCORD_GUILD_NAME')
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
PREFIX = "!"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == DISCORD_GUILD_NAME, bot.guilds) # TODO: check if find will throw an error
    if guild:
        print(
            f'{bot.user} is connected to the following guild:\n',
            f'{guild.name}(id: {guild.id})'
        )   

@bot.event 
async def on_member_join(member):
    guild = discord.utils.find(lambda g: g.name == DISCORD_GUILD_NAME, bot.guilds) # TODO: check if find will throw an error
    welcome_channel = discord.utils.find(lambda c: c.name == "👋welcome", guild.channels) # TODO: remove welcome channel hardcod

    http_response = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q=welcome&limit=25&offset=0&rating=pg-13&lang=en")
    welcome_gifs = json.loads(http_response.text)
    welcome_gif = random.choice(welcome_gifs["data"])

    gif_embed = discord.Embed()
    gif_embed.set_image(url=welcome_gif["images"]["original"]["url"])

    await welcome_channel.send(embed=gif_embed)
    await welcome_channel.send(f"<@!{member.id}> **Welcome to {DISCORD_GUILD_NAME}!** :wave:")

@bot.event
async def on_message(message):
    # avoid bot self trigger
    if message.author == bot.user:
        return

    # repsond with command prefix
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        await message.channel.send(f"**Learn more about me by running:** `{PREFIX}help`")

    # allow cogs to handle messages too
    await bot.process_commands(message)

# override default help command
menu = DefaultMenu('◀️', '▶️', '❌')
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green()) 

# commands by category a.k.a. cogs
bot.add_cog(Python())
bot.add_cog(Fun())
bot.add_cog(Finance())

# start up bot
bot.run(DISCORD_BOT_TOKEN)