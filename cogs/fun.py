import random
import discord
import requests
import json
import requests
from discord.ext import commands

class Fun(commands.Cog):
    """Commands that are good for the soul!"""

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