import discord
import requests
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

# load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_NAME = os.getenv('DISCORD_GUILD_NAME')
LUNAR_CRUSH_API_KEY = os.getenv('LUNAR_CRUSH_API_KEY')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == DISCORD_GUILD_NAME, bot.guilds)
    if guild:
        print(
            f'{bot.user} is connected to the following guild:\n',
            f'{guild.name}(id: {guild.id})'
        )   

@bot.event
async def on_message(message):
    # ignore messages from the bot itself
    if message.author == bot.user:
        return

    msg_str = message.content

    # Help command
    if msg_str == '!help':
        await message.channel.send("!help - Displays this help message")

    # Resources command
    if msg_str == "!resources":
        await message.channel.send("Some resources for you here!")

    # Crypto command
    if msg_str.startswith("!crypto"):
        symbols = ["BTC", "ETH", "LTC"]

        # make the call for prices
        http_response = requests.get("https://api.lunarcrush.com/v2?data=assets&key=" + LUNAR_CRUSH_API_KEY + "&symbol=" + ",".join(symbols))
        data = json.loads(http_response.text)

        # extract prices
        prices = []
        prices.append(int(data["data"][0]["price"])) # BTC
        prices.append(int(data["data"][1]["price"])) # ETH
        prices.append(int(data["data"][2]["price"])) # LTC

        # derive message response
        msg_response = "Cryptocurrency prices for today!\n"
        for i in range(len(symbols)):
            msg_response += "**{}** - ${}\n".format(symbols[i], prices[i])

        await message.channel.send(msg_response)

bot.run(DISCORD_BOT_TOKEN)