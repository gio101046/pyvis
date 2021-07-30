from os import name
import random
import discord
from discord.ext.commands.core import command
import requests
import json
import requests
from data import poll_cache
from datetime import date
from discord.ext import commands

class Fun(commands.Cog):
    """Commands that are good for the soul!"""

    OPTION_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    FULL_CHAR = "█"
    BAR_LENGTH = 20

    @commands.command()
    async def flip(self, ctx) -> None:
        """Flips a coin and return either heads or tails."""

        coin = random.randint(0, 1)
        message = "heads!" if coin else "tails!"
        await ctx.send(f"<@!{ctx.author.id}> {message}")

    @commands.command(usage="<repo_name>")
    async def github(self, ctx, repo_name: str = "") -> None:
        """Returns the github repo information for a given repo name."""

        if len(repo_name.strip()) == 0:
            await ctx.send("**Please provide a repo name. ex.** `!github gio101046/pyvis`")
            return

        http_response = requests.get(f"https://api.github.com/repos/{repo_name}")
        repo_info = json.loads(http_response.text)

        if http_response.status_code == 404: 
            await ctx.send(f"**Couldn't find repo:** `{repo_name}`")
            return

        # construct embed response
        github_embed = discord.Embed(title=repo_info["full_name"], description=repo_info["description"], color=0x3DCCDD) # TODO: extract harcoded color
        github_embed.set_thumbnail(url=repo_info["owner"]["avatar_url"])
        github_embed.add_field(name="Repository", value=f"[{repo_info['name']}]({repo_info['html_url']})", inline=True)
        github_embed.add_field(name="Language", value=repo_info['language'], inline=True)
        github_embed.add_field(name="Forks", value=repo_info['forks'], inline=True)
        github_embed.add_field(name="Watchers", value=repo_info['watchers'], inline=True)
        github_embed.add_field(name="Open Issues", value=repo_info['open_issues'], inline=True)
        github_embed.set_footer(text=f"Repo created at • {repo_info['created_at'].split('T')[0]}")

        await ctx.send(embed=github_embed)

    @commands.group(invoke_without_command=True)
    async def poll(self, ctx) -> None:
        """Allows for creating polls and querying results."""
        await ctx.send("**poll create ->**  `!poll create \"My question?\" option1 option2`")
        await ctx.send("**poll results ->** `!poll results 870733802190807050`")

    @poll.command(usage="\"<question>\" <options>", name="create")
    async def poll_create(self, ctx, *params: str) -> None:
        """Creates a poll with the given parameters."""

        if len(params) <= 1:
            await ctx.send("**Please provide the parameters for the poll. ex.** `!poll \"My question?\" option1 option2`")
            return

        question = params[0]
        options = params[1:]

        # create embed response
        poll_embed = discord.Embed(title=question, description="\u200b", color=0x3DCCDD)
        for i in range(len(options)):
            poll_embed.add_field(value="\u200b", name=f"{self.OPTION_EMOJIS[i]} {options[i]}", inline=False)
        poll_embed.set_footer(text=f"Poll created on • {date.today().strftime('%m/%d/%y')}")

        message = await ctx.send(embed=poll_embed)

        # add poll to cache
        poll_cache[message.id] = {}
        for i in range(len(options)):
            poll_cache[message.id][f"{self.OPTION_EMOJIS[i]}"] = []
        poll_cache[message.id]["question"] = question
        poll_cache[message.id]["options"] = ",".join(options)

        # add option emojis to poll
        for i in range(len(options)):
            await message.add_reaction(self.OPTION_EMOJIS[i])

    @poll.command(usage="<message_id>", name="results")
    async def poll_results(self, ctx, message_id: int = None) -> None:
        """Shows results of a poll given a message id."""
        
        if not message_id:
            await ctx.send("**Please provide the message id of a poll. ex.** `!poll results 870733802190807050")
            return

        if message_id not in poll_cache:
            await ctx.send("**Could not find poll with that message id.**")
            return

        poll = poll_cache[message_id]
        question = poll["question"]
        options = poll["options"].split(",")

        total_votes = sum([0 if item[0] == "question" or item[0] == "options" else len(item[1]) for item in poll.items()])
        option_percentages = []
        for i in range(len(options)):
            option_votes = len(poll[self.OPTION_EMOJIS[i]])
            option_percentages.append(0 if total_votes == 0 else option_votes / total_votes)

        # construct embed response
        results_embed = discord.Embed(title=question, description="🥁", color=0x3DCCDD)
        for i in range(len(options)):
            str_bar = "".join([self.FULL_CHAR for _ in range(int(self.BAR_LENGTH * option_percentages[i]))])
            str_percent = f"{option_percentages[i] * 100:.2f}%"
            str_votes = f"({int(option_percentages[i] * total_votes)} votes)"
            results_embed.add_field(name=f"{self.OPTION_EMOJIS[i]} {options[i]}", value=f"{str_bar} {str_percent} {str_votes}", inline=False)
        results_embed.set_footer(text=f"Poll queried on • {date.today().strftime('%m/%d/%y')}")

        await ctx.send(embed=results_embed)
