import logging
import re

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from core import Cog, Context, CustomCommand


class CustomCommandModal(discord.ui.Modal):
    command_name: str
    content: str

    def __init__(self, title: str, name_value: str = "", content_value: str = ""):
        super().__init__(title=title)
        self.add_item(
            discord.ui.InputText(
                label="Command Name",
                placeholder="lootpolicy",
                value=name_value,
                max_length=50,
                required=True,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Command Content",
                placeholder="Enter the markdown content for this command...",
                value=content_value,
                style=discord.InputTextStyle.long,
                max_length=4000,
                required=True,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        # Store the values for later use
        self.command_name = self.children[0].value or ""
        self.content = self.children[1].value or ""
        await interaction.response.defer()


class ConfirmDeleteView(discord.ui.View):
    def __init__(self, command_name: str):
        super().__init__(timeout=30)
        self.command_name = command_name
        self.confirmed = False

    @discord.ui.button(label="Confirm Delete", style=discord.ButtonStyle.danger)
    async def confirm_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.confirmed = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.confirmed = False
        self.stop()


class CustomCommands(Cog):
    """Commands for managing custom guild commands."""

    def __init__(self, bot):
        super().__init__(bot)
        self.logger = logging.getLogger(__name__)

    newcommand = SlashCommandGroup(
        "newcommand",
        "Manage custom commands",
        contexts={discord.InteractionContextType.guild},
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @newcommand.command(name="create", description="Create a new custom command")
    async def create_command(self, ctx: Context):
        """Create a new custom command using a modal."""
        assert ctx.guild

        modal = CustomCommandModal(title="Create Custom Command")
        await ctx.send_modal(modal)
        await modal.wait()

        # Validate command name
        command_name = modal.command_name.lower().strip()
        if not re.match(r"^[a-z0-9_]+$", command_name):
            return await ctx.error(
                "Invalid Command Name",
                "Command names can only contain lowercase letters, numbers, and underscores.",
                ephemeral=True,
            )

        # Check for duplicate
        existing = await CustomCommand.get_or_none(
            discord_guild_id=ctx.guild.id, command_name=command_name
        )
        if existing:
            return await ctx.error(
                "Command Already Exists",
                f"A command named `{command_name}` already exists. Use `/newcommand edit` to modify it.",
                ephemeral=True,
            )

        # Create the command
        await CustomCommand.create(
            discord_guild_id=ctx.guild.id,
            command_name=command_name,
            content=modal.content,
            created_by=ctx.author.id,
        )

        await ctx.success(
            "Command Created",
            f"Custom command `!{command_name}` has been created successfully.",
            ephemeral=True,
        )

    @newcommand.command(name="list", description="List all custom commands")
    async def list_commands(self, ctx: Context):
        """List all custom commands for this guild."""
        assert ctx.guild

        commands_list = await CustomCommand.filter(
            discord_guild_id=ctx.guild.id
        ).all()

        if not commands_list:
            return await ctx.info(
                "No Custom Commands",
                "No custom commands have been created yet. Use `/newcommand create` to add one.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title=f"Custom Commands ({len(commands_list)})",
            color=discord.Color.blurple(),
        )

        command_names = [f"`!{cmd.command_name}`" for cmd in commands_list]
        embed.description = ", ".join(command_names)

        await ctx.respond(embed=embed, ephemeral=True)

    @newcommand.command(
        name="view", description="View the content of a custom command"
    )
    @discord.option(
        "name", str, description="The name of the command to view", required=True
    )
    async def view_command(self, ctx: Context, name: str):
        """View a specific custom command's content."""
        assert ctx.guild

        command_name = name.lower().strip()
        command = await CustomCommand.get_or_none(
            discord_guild_id=ctx.guild.id, command_name=command_name
        )

        if not command:
            return await ctx.error(
                "Command Not Found",
                f"No custom command named `{command_name}` exists.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title=f"Command: !{command.command_name}", color=discord.Color.blurple()
        )
        embed.add_field(name="Content", value=command.content, inline=False)
        embed.set_footer(text=f"Created by ID: {command.created_by}")
        embed.timestamp = command.created_at

        await ctx.respond(embed=embed, ephemeral=True)

    @newcommand.command(name="edit", description="Edit an existing custom command")
    @discord.option(
        "name", str, description="The name of the command to edit", required=True
    )
    async def edit_command(self, ctx: Context, name: str):
        """Edit an existing custom command."""
        assert ctx.guild

        command_name = name.lower().strip()
        command = await CustomCommand.get_or_none(
            discord_guild_id=ctx.guild.id, command_name=command_name
        )

        if not command:
            return await ctx.error(
                "Command Not Found",
                f"No custom command named `{command_name}` exists.",
                ephemeral=True,
            )

        # Pre-fill modal with existing data
        modal = CustomCommandModal(
            title="Edit Custom Command",
            name_value=command.command_name,
            content_value=command.content,
        )
        await ctx.send_modal(modal)
        await modal.wait()

        # Validate new command name
        new_command_name = modal.command_name.lower().strip()
        if not re.match(r"^[a-z0-9_]+$", new_command_name):
            return await ctx.error(
                "Invalid Command Name",
                "Command names can only contain lowercase letters, numbers, and underscores.",
                ephemeral=True,
            )

        # Check if renaming to an existing command
        if new_command_name != command.command_name:
            existing = await CustomCommand.get_or_none(
                discord_guild_id=ctx.guild.id, command_name=new_command_name
            )
            if existing:
                return await ctx.error(
                    "Command Already Exists",
                    f"A command named `{new_command_name}` already exists.",
                    ephemeral=True,
                )

        # Update the command
        command.command_name = new_command_name
        command.content = modal.content
        await command.save()

        await ctx.success(
            "Command Updated",
            f"Custom command `!{new_command_name}` has been updated successfully.",
            ephemeral=True,
        )

    @newcommand.command(name="delete", description="Delete a custom command")
    @discord.option(
        "name", str, description="The name of the command to delete", required=True
    )
    async def delete_command(self, ctx: Context, name: str):
        """Delete a custom command with confirmation."""
        assert ctx.guild

        command_name = name.lower().strip()
        command = await CustomCommand.get_or_none(
            discord_guild_id=ctx.guild.id, command_name=command_name
        )

        if not command:
            return await ctx.error(
                "Command Not Found",
                f"No custom command named `{command_name}` exists.",
                ephemeral=True,
            )

        # Show confirmation view
        view = ConfirmDeleteView(command_name)
        embed = discord.Embed(
            title="Confirm Deletion",
            description=f"Are you sure you want to delete the custom command `!{command_name}`?",
            color=discord.Color.orange(),
        )

        await ctx.respond(embed=embed, view=view, ephemeral=True)
        await view.wait()

        if view.confirmed:
            await command.delete()
            await ctx.edit(
                embed=discord.Embed(
                    title="Command Deleted",
                    description=f"Custom command `!{command_name}` has been deleted.",
                    color=discord.Color.green(),
                ),
                view=None,
            )
        else:
            await ctx.edit(
                embed=discord.Embed(
                    title="Deletion Cancelled",
                    description=f"Custom command `!{command_name}` was not deleted.",
                    color=discord.Color.blurple(),
                ),
                view=None,
            )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listen for custom command triggers."""
        self.logger.debug(f"on_message triggered: '{message.content}' from {message.author} in {message.guild}")

        # Ignore bot messages
        if message.author.bot:
            self.logger.debug(f"Ignoring bot message from {message.author}")
            return

        # Only process messages in guilds
        if not message.guild:
            self.logger.debug("Ignoring DM message")
            return

        # Check if message starts with !
        if not message.content.startswith("!"):
            self.logger.debug(f"Message doesn't start with '!': '{message.content}'")
            return

        self.logger.debug(f"Message starts with '!': '{message.content}'")

        # Extract command name (everything after ! until first space or end of string)
        parts = message.content[1:].split(maxsplit=1)
        if not parts:
            self.logger.debug("No command name found after '!'")
            return

        command_name = parts[0].lower()
        self.logger.debug(f"Extracted command name: '{command_name}'")

        # Look up the command
        self.logger.debug(f"Looking up command '{command_name}' in guild {message.guild.id}")
        command = await CustomCommand.get_or_none(
            discord_guild_id=message.guild.id, command_name=command_name
        )

        if command:
            self.logger.debug(f"Command '{command_name}' found! Sending reply with content: {command.content[:50]}...")
            # Send ephemeral response with the command content
            await message.reply(command.content, mention_author=False)
            self.logger.debug(f"Reply sent for command '{command_name}'")
        else:
            self.logger.debug(f"Command '{command_name}' not found in database for guild {message.guild.id}")


def setup(bot):
    bot.add_cog(CustomCommands(bot))
