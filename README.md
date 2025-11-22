# Banshee Bot

A Discord bot for World of Warcraft guild management, built with Python and Pycord.

## Features

- Guild settings management (guild name, region, realm)
- Custom commands system for guild resources and information
- More features coming soon!

## Setup

### Prerequisites

- Python 3.11+
- A Discord bot token ([Create one here](https://discord.com/developers/applications))

### Installation

1. Clone or download this repository

2. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies:
```bash
uv sync
```

4. Configure environment:
```bash
cp .env.example .env
```
Edit `.env` and add your Discord bot token.

5. Run the bot:
```bash
uv run main.py --sync
```

## Usage

### Settings Commands

All settings commands require administrator permissions.

- `/settings show` - Display current guild settings
- `/settings guild <guild_name> <region> <realm>` - Set your WoW guild information

Example:
```
/settings guild "Awesome Guild" us "Area 52"
```

### Custom Commands

Custom commands allow guild admins to create reusable commands that any member can trigger with the `!` prefix. Perfect for loot policies, guild rules, helpful links, and more.

#### Management Commands (Admin Only)

- `/newcommand create` - Opens a form to create a new custom command
- `/newcommand list` - Shows all custom commands for your guild
- `/newcommand view <name>` - View the content of a specific command
- `/newcommand edit <name>` - Edit an existing command (opens pre-filled form)
- `/newcommand delete <name>` - Delete a command (requires confirmation)

#### Using Custom Commands

Any member can trigger custom commands:
```
!lootpolicy
!raidtimes
!resources
```

**Features:**
- Command responses are sent as replies (visible to everyone)
- Supports full Discord markdown formatting
- Command names must be lowercase alphanumeric with underscores only
- Each guild has its own set of custom commands

**Example Workflow:**
1. Admin runs `/newcommand create`
2. In the form, enters name: `lootpolicy` and content: `**Loot Policy**: All gear is distributed via council...`
3. Members can now use `!lootpolicy` to see the policy

## Project Structure
```
banshee-bot/
├── main.py                  # Entry point
├── core/                    # Core bot functionality
│   ├── bot.py              # Bot class
│   ├── context.py          # Custom context
│   └── models.py           # Database models
├── cogs/                    # Command modules
│   ├── settings.py         # Settings commands
│   └── custom_commands.py  # Custom commands system
└── data/                    # SQLite database (auto-generated)
```

## Tech Stack

- **Discord Library**: Pycord
- **Package Manager**: uv
- **Database**: SQLite (local) / PostgreSQL (production) with Tortoise ORM
- **Environment**: python-dotenv


## Local Development

### Running Locally

The bot uses SQLite by default for local development (no external database needed):

```bash
# Normal run
uv run main.py

# Sync commands with Discord (required after adding/modifying slash commands)
uv run main.py --sync

# Debug mode with separate bot token
uv run main.py --debug
```

### Environment Configuration

Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

**Minimal local setup:**
```env
DISCORD_TOKEN=your_development_bot_token
```

**With debug token:**
```env
DISCORD_TOKEN=your_development_bot_token
DEBUG_TOKEN=your_debug_bot_token
```

The bot will automatically use SQLite (`data/database.db`) when `DATABASE_URL` is not set.
