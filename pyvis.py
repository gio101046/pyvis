import discord
import requests
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_NAME = os.getenv('DISCORD_GUILD_NAME')
LUNAR_CRUSH_API_KEY = os.getenv('LUNAR_CRUSH_API_KEY')
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == DISCORD_GUILD_NAME, bot.guilds)
    if guild:
        print(
            f'{bot.user} is connected to the following guild:\n',
            f'{guild.name}(id: {guild.id})'
        )   

@bot.command(name="resources")
async def resources(ctx):
    await ctx.send("Some resources for you here!")

@bot.command(name="stock")
async def stock(ctx, *tickers):
    if len(tickers) == 0:
        tickers = ["AAPL", "GOOG", "MSFT", "AMZN"]

    # msg response setup
    msg_response = "Stock prices for today!\n"
    stock_found = False

    # make the call for stock prices
    for ticker in tickers:
        http_response = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHAVANTAGE_API_KEY}')
        stock_data = json.loads(http_response.text)

        # check if stock exists
        if 'Global Quote' not in stock_data:
            continue

        # get the stock price
        stock_price = stock_data['Global Quote']['05. price']
        msg_response += f'**{ticker}**: ${round(float(stock_price), 2)}\n'  
        stock_found = True


    if not stock_found:
        await ctx.send("No stock data found for given tickers!")
        return

    await ctx.send(msg_response) 

@bot.command(name="crypto")
async def crypto(ctx, *tickers):
    # default tickers
    if len(tickers) == 0:
        tickers = ["BTC", "ETH", "LTC"]

    # make the call for prices
    http_response = requests.get(f"https://api.lunarcrush.com/v2?data=assets&key={LUNAR_CRUSH_API_KEY}&symbol={','.join(tickers)}")
    data = json.loads(http_response.text)

    # extract prices and derive message response
    msg_response = "Cryptocurrency prices for today!\n"
    msg_response += "\n".join([f"**{item['symbol']}**: ${round(float(item['price']), 2)}" for item in data["data"]])

    await ctx.send(msg_response)

bot.run(DISCORD_BOT_TOKEN)