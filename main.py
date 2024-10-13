"""
Main Module of the Manager and helper-bot-manager.
"""
import logging
import asyncio
import sys
from manager_cw_bot_api.business import run


# Do not break the structure of func-s, classes, and components to make the modules work correctly.
async def main() -> None:
    """Main Function (run bot)."""
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(levelname)s: %(asctime)s -- %(funcName)s -- %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

    await run()


if __name__ == '__main__':
    asyncio.run(main())
