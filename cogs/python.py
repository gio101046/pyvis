from discord.ext import commands

class Python(commands.Cog):
    """General commands about python programming."""

    @commands.command()
    async def resources(self, ctx):
        """
            Will provide resources for python programming.
        """
        await ctx.send("Some resources for you here!") # TODO: Add resources