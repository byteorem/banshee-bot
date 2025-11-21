# Banshee Bot

A Discord bot for World of Warcraft guild management, built with Python and Pycord.

## Features

- Guild settings management (guild name, region, realm)
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

## Project Structure
```
banshee-bot/
├── main.py              # Entry point
├── core/                # Core bot functionality
│   ├── bot.py          # Bot class
│   ├── context.py      # Custom context
│   └── models.py       # Database models
├── cogs/                # Command modules
│   └── settings.py     # Settings commands
└── data/                # SQLite database (auto-generated)
```

## Tech Stack

- **Discord Library**: Pycord
- **Package Manager**: uv
- **Database**: SQLite with Tortoise ORM
- **Environment**: python-dotenv
