"""
Main Module of the Manager and helper-bot-manager.
"""
import logging
import asyncio
import sys
from manager_cw_bot_api.business import run


async def main() -> None:
    """Main Function (run bot)."""
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await run()


if __name__ == '__main__':
    asyncio.run(main())
