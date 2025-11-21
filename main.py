from argparse import ArgumentParser
from dotenv import load_dotenv
import logging

from core import Banshee


if __name__ == "__main__":
    parser = ArgumentParser(prog="Banshee")
    parser.add_argument(
        "-d",
        "--debug",
        dest="cogs",
        action="extend",
        nargs="*",
        help="run in debug mode",
    )
    parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help="synchronize commands",
    )
    args = parser.parse_args()
    debug = args.cogs is not None

    load_dotenv(".env")

    # Configure discord library logging (file only)
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    file_handler = logging.FileHandler(
        filename="discord.log", encoding="utf-8", mode="w"
    )
    file_handler.formatter = logging.Formatter(
        "[%(asctime)s %(levelname)s] %(name)s: %(message)s",
        "%d/%m/%y %H:%M:%S",
    )
    discord_logger.addHandler(file_handler)

    # Configure cogs logging (console output for debugging)
    cogs_logger = logging.getLogger("cogs")
    cogs_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "[%(asctime)s %(levelname)s] %(name)s: %(message)s",
        "%d/%m/%y %H:%M:%S",
    ))
    cogs_logger.addHandler(console_handler)

    bot = Banshee()
    bot.run(debug=debug, cogs=args.cogs, sync=args.sync)