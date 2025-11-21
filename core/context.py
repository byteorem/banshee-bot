from discord import ApplicationContext, Color, Embed
from discord.utils import utcnow


class Context(ApplicationContext):
    async def success(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title,
            description=description,
            timestamp=utcnow(),
            color=Color.green(),
        )
        return await self.respond(embed=embed, **kwargs)

    async def error(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title,
            description=description,
            timestamp=utcnow(),
            color=Color.red(),
        )
        return await self.respond(embed=embed, **kwargs)

    async def info(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title,
            description=description,
            timestamp=utcnow(),
            color=Color.blurple(),
        )
        return await self.respond(embed=embed, **kwargs)