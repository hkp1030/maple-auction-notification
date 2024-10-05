import asyncio

import config
import message
import search
from logger import logger


async def main():
    logger.info('Start Maple Auction Notification')
    interval = config.INTERVAL_SEC
    shown_items = set()
    while True:
        items = search.search_items()
        logger.info(f'Found {len(items)} items')
        for item in items:
            if item['seq'] in shown_items:
                continue
            shown_items.add(item['seq'])
            text = search.format_item(item)
            await message.send_message(text)
        await asyncio.sleep(interval)


if __name__ == '__main__':
    asyncio.run(main())
