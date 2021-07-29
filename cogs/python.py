from discord.ext import commands

class Python(commands.Cog):
    """Commands about python programming."""

    @commands.command()
    async def resources(self, ctx) -> None:
        """Will provide resources for python programming."""
        await ctx.send("Some resources for you here!") # TODO: Add resources