import os
import requests
import json
from discord.ext import commands

class Finance(commands.Cog):
    """Commands to query stock and crypto prices."""

    @commands.command(usage="[tickers]")
    async def stock(self, ctx, *tickers):
        """
            Get prices for the given stock tickers. Will default tickers to AAPL, GOOG, MSFT and AMZN if none provided.
        """
        ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

        if len(tickers) == 0:
            tickers = ["AAPL", "GOOG", "MSFT", "AMZN"]

        # msg response setup
        msg_response = ""
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

    @commands.command(usage="[tickers]")
    async def crypto(self, ctx, *tickers):
        """
            Get prices for the given crypto tickers. Will default tickers to BTC, ETH and LTC if none provided.
        """
        LUNAR_CRUSH_API_KEY = os.getenv('LUNAR_CRUSH_API_KEY')

        # default tickers
        if len(tickers) == 0:
            tickers = ["BTC", "ETH", "LTC"]

        # make the call for prices
        http_response = requests.get(f"https://api.lunarcrush.com/v2?data=assets&key={LUNAR_CRUSH_API_KEY}&symbol={','.join(tickers)}")
        data = json.loads(http_response.text)

        # extract prices and derive message response
        msg_response = ""
        msg_response += "\n".join([f"**{item['symbol']}**: ${round(float(item['price']), 2)}" for item in data["data"]])

        await ctx.send(msg_response)