import discord

client = discord.Client()

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):
    msg_str = message.content
    print(msg_str)
    pass

client.run("") # pass the bot token here

"""
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('token')
"""