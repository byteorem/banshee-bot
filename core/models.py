from tortoise import fields
from tortoise.models import Model

__all__ = ("GuildSettings",)


class GuildSettings(Model):
    id = fields.IntField(pk=True)
    discord_guild_id = fields.BigIntField(unique=True)
    wow_guild_name = fields.CharField(max_length=255, null=True)
    wow_region = fields.CharField(max_length=10, null=True)
    wow_realm = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "guild_settings"