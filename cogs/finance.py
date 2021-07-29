import os
import requests
import json
from discord.ext import commands

LUNAR_CRUSH_API_KEY = os.getenv('LUNAR_CRUSH_API_KEY')
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

class Finance(commands.Cog):
    """Commands to query stock and crypto prices"""

    @commands.command()
    async def stock(ctx, *tickers):
        """!stock [tickers] - example usage '!stock TSLA GOOG'"""

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

    @commands.command()
    async def crypto(ctx, *tickers):
        """!crypto [tickers] - example usage '!crypto BTC LTC'"""

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