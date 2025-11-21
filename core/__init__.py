from discord.ext import commands

from .bot import Banshee
from .context import Context
from .models import GuildSettings

__all__ = (
    "Banshee",
    "Cog",
    "Context",
    "GuildSettings",
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: Banshee) -> None:
        self.bot = bot