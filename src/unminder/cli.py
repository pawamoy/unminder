"""Module that contains the command line application."""

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

from __future__ import annotations

import argparse
import sys
from typing import Any

from telethon import TelegramClient


from unminder import debug


class _DebugInfo(argparse.Action):
    def __init__(self, nargs: int | str | None = 0, **kwargs: Any) -> None:
        super().__init__(nargs=nargs, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        debug.print_debug_info()
        sys.exit(0)



def get_user_credentials():
    """Utility function to get a user's credentials from environment variables."""
    try:
        username = os.environ["TELEGRAM_USERNAME"]
        api_id = int(os.environ["TELEGRAM_API_ID"])
        api_hash = os.environ["TELEGRAM_API_HASH"]
    except (TypeError, KeyError):
        print(
            "error: Please set the following environment variables:\n"
            "TELEGRAM_USERNAME, TELEGRAM_API_ID, TELEGRAM_API_HASH",
            file=sys.stderr,
        )
        sys.exit(1)
    return username, api_id, api_hash
def review(args=None):
    """The review command."""
    parser = argparse.ArgumentParser(prog="review")
    opts = parser.parse_args(args=args)  # noqa

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


def get_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(prog="unminder")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {debug.get_version()}")
    parser.add_argument("--debug-info", action=_DebugInfo, help="Print debug information.")
    return parser


def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `unminder` or `python -m unminder`.

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args=args)
    print(opts)
    return 0
