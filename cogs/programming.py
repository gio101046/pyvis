from discord.ext import commands

class Programming(commands.Cog):
    """Commands about programming."""

    @commands.command()
    async def resources(self, ctx) -> None:
        """Will provide resources for programming."""
        await ctx.send("Some resources for you here!") # TODO: Add resources