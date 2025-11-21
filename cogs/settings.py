import discord
from discord.commands import SlashCommandGroup

from core import Cog, Context, GuildSettings


class Settings(Cog):
    """Commands for managing server settings."""

    settings = SlashCommandGroup(
        "settings",
        "Manage server settings",
        contexts={discord.InteractionContextType.guild},
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @settings.command(name="show", description="Show current server settings")
    async def show_settings(self, ctx: Context):
        """Show current server settings."""
        assert ctx.guild
        settings = await GuildSettings.get_or_none(discord_guild_id=ctx.guild.id)

        if not settings or not settings.wow_guild_name:
            return await ctx.info(
                "No Settings Found",
                "No guild settings configured yet. Use `/settings guild` to set up.",
            )

        embed = discord.Embed(title="Server Settings", color=discord.Color.blurple())
        embed.add_field(
            name="Guild Name", value=settings.wow_guild_name, inline=False
        )
        embed.add_field(name="Region", value=settings.wow_region.upper(), inline=True)
        embed.add_field(name="Realm", value=settings.wow_realm, inline=True)
        embed.set_footer(text=f"Last updated")
        embed.timestamp = settings.updated_at

        await ctx.respond(embed=embed)

    @settings.command(name="guild", description="Set WoW guild information")
    @discord.option("guild_name", str, description="The name of your WoW guild")
    @discord.option("region", str, description="Region (us, eu, kr, tw, cn)")
    @discord.option("realm", str, description="Realm name")
    async def set_guild(
        self,
        ctx: Context,
        guild_name: str,
        region: str,
        realm: str,
    ):
        """Set WoW guild information."""
        assert ctx.guild
        settings, created = await GuildSettings.get_or_create(
            discord_guild_id=ctx.guild.id
        )

        settings.wow_guild_name = guild_name
        settings.wow_region = region.lower()
        settings.wow_realm = realm
        await settings.save()

        action = "created" if created else "updated"
        await ctx.success(
            f"Guild Settings {action.title()}",
            f"**{guild_name}** - {region.upper()} - {realm}",
        )


def setup(bot):
    bot.add_cog(Settings(bot))