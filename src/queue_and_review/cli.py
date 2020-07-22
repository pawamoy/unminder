# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m unminder` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `unminder.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `unminder.__main__` in `sys.modules`.

"""Module that contains the command line application."""

import argparse
import os
import sys

from telethon import TelegramClient, events, sync


def get_user_credentials():
    try:
        username = os.environ["TELEGRAM_USERNAME"]
        api_id = int(os.environ["TELEGRAM_API_ID"])
        api_hash = os.environ["TELEGRAM_API_HASH"]
    except (TypeError, KeyError):
        print("error: Please set the following environment variables:\n"
              "TELEGRAM_USERNAME, TELEGRAM_API_ID, TELEGRAM_API_HASH", file=sys.stderr)
        sys.exit(1)
    return username, api_id, api_hash


def get_parser():
    """Return the CLI argument parser."""
    return argparse.ArgumentParser(prog="queue")


def queue(args=None):
    """The queue command."""
    parser = get_parser()
    opts = parser.parse_args(args=args)
    print(opts)
    return 0


def review(args=None):
    """The review command."""
    parser = get_parser()
    opts = parser.parse_args(args=args)

    username, api_id, api_hash = get_user_credentials()
    client = TelegramClient("review", api_id, api_hash)
    client.start()

    messages = list(reversed(client.iter_messages(username)))
    print(len(messages))

    download_media = False
    for message in messages:
        if not message.message:
            if download_media:
                media = message.download_media()
                if media:
                    print(media)
        else:
            print(message.message)
            print()

    return 0
