import discord
import os
from discord.flags import MessageFlags
import requests
import json
import random
from cogs import Programming
from cogs import Fun
from cogs import Finance
from data import poll_cache
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
intents.reactions = True
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
    """ WELCOME START """
    guild = discord.utils.find(lambda g: g.name == DISCORD_GUILD_NAME, bot.guilds) # TODO: check if find will throw an error
    welcome_channel = discord.utils.find(lambda c: c.name == "👋welcome", guild.channels) # TODO: remove welcome channel hardcode

    http_response = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q=welcome&limit=25&offset=0&rating=pg-13&lang=en")
    welcome_gifs = json.loads(http_response.text)
    welcome_gif = random.choice(welcome_gifs["data"])

    gif_embed = discord.Embed()
    gif_embed.set_image(url=welcome_gif["images"]["original"]["url"])

    await welcome_channel.send(embed=gif_embed)
    await welcome_channel.send(f"<@!{member.id}> **Welcome to {DISCORD_GUILD_NAME}!** :wave:")
    """ WELCOME END """

@bot.event
async def on_message(message):
    # avoid bot self trigger
    if message.author == bot.user:
        return

    # TODO: is channel is a proposal channel check for poll command

    # repsond with command prefix
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        await message.channel.send(f"**Learn more about me by running:** `{PREFIX}help`")

    # allow cogs to handle messages too
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(event):
    # avoid bot self trigger
    if event.user_id == bot.user.id:
        return

    """ POLL START """
    # check if message is in cache and if reaction is valid
    if event.message_id in poll_cache and event.emoji.name in Fun.OPTION_EMOJIS:
        # if user has not voted yet, add their vote
        if event.user_id not in poll_cache[event.message_id][event.emoji.name]:
            poll_cache[event.message_id][event.emoji.name].append(event.user_id)
    """ POLL END """

    print(poll_cache)

@bot.event
async def on_raw_reaction_remove(event):
    # avoid bot self trigger
    if event.user_id == bot.user.id:
        return

    """ POLL START """
    # check if message is in cache and if reaction is valid
    if event.message_id in poll_cache and event.emoji.name in Fun.OPTION_EMOJIS:
        # if user has voted, remove their vote
        if event.user_id in poll_cache[event.message_id][event.emoji.name]:
            poll_cache[event.message_id][event.emoji.name].remove(event.user_id)
    """ POLL END """

    print(poll_cache)

# override default help command
menu = DefaultMenu('◀️', '▶️', '❌')
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green()) 

# commands by category a.k.a. cogs
bot.add_cog(Programming())
bot.add_cog(Fun())
bot.add_cog(Finance())

# start up bot
bot.run(DISCORD_BOT_TOKEN)