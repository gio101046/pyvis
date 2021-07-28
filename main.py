import discord
import requests
import json

LUNAR_CRUSH_API_KEY = "LUNAR_API_KEY"

client = discord.Client()

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):
    msg_str = message.content

    # Help command
    if msg_str == '!help':
        await message.channel.send("!help - Displays this help message")

    # Resources command
    if msg_str == "!resources":
        await message.channel.send("Some resources for you here!")

    # Crypto command
    if msg_str == "!crypto":
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

client.run("DISCORD_TOKEN") # pass the bot token here