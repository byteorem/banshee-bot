import logging
from os import environ, getenv, makedirs

import discord
from discord.ext import commands
from tortoise import Tortoise

from .context import Context

logger = logging.getLogger(__name__)


class Banshee(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(
            auto_sync_commands=False,
            help_command=None,
            intents=intents
        )

    async def setup_tortoise(self) -> None:
        db_url = getenv("DATABASE_URL", "sqlite://data/database.db")

        # Only create data directory for SQLite
        if db_url.startswith("sqlite"):
            makedirs("data", exist_ok=True)
            logger.info("Using SQLite database (local development)")
        else:
            logger.info(f"Using PostgreSQL database (production)")

        await Tortoise.init(
            db_url=db_url, modules={"models": ["core.models"]}
        )
        await Tortoise.generate_schemas()

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        await self.setup_tortoise()
        return await super().start(token, reconnect=reconnect)

    async def close(self) -> None:
        await Tortoise.close_connections()
        return await super().close()

    async def get_application_context(
        self, interaction: discord.Interaction, cls: type[Context] = Context
    ) -> Context:
        return cls(self, interaction)

    async def on_ready(self) -> None:
        print(f"{self.user} is ready")

    async def on_application_command_error(self, context: discord.ApplicationContext, exception: Exception):
        if isinstance(exception, discord.ApplicationCommandInvokeError):
            exception = exception.original

        await context.respond(
            embed=discord.Embed(
                title=exception.__class__.__name__,
                description=str(exception),
                color=discord.Color.red(),
            )
        )

    def run(
        self, debug: bool = False, cogs: list[str] | None = None, sync: bool = False
    ) -> None:
        self.load_extensions(*cogs or ("cogs",))

        if sync:
            async def on_connect() -> None:
                await self.sync_commands(delete_existing=not debug)
                print("Synchronized commands.")

            self.on_connect = on_connect

        token = getenv("DEBUG_TOKEN" if debug else "DISCORD_TOKEN", getenv("DISCORD_TOKEN"))

        if not token:
            raise ValueError("DISCORD_TOKEN environment variable is required")

        super().run(token)