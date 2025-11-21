from tortoise import fields
from tortoise.models import Model

__all__ = ("GuildSettings", "CustomCommand")


class GuildSettings(Model):
    id = fields.IntField(pk=True)
    discord_guild_id = fields.BigIntField(unique=True)
    wow_guild_name = fields.CharField(max_length=255, null=True)
    wow_region = fields.CharField(max_length=10, null=True)
    wow_realm = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:  # type: ignore
        table = "guild_settings"


class CustomCommand(Model):
    id = fields.IntField(pk=True)
    discord_guild_id = fields.BigIntField()
    command_name = fields.CharField(max_length=50)
    content = fields.TextField()
    created_by = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:  # type: ignore
        table = "custom_commands"
        unique_together = (("discord_guild_id", "command_name"),)