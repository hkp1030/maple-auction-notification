import asyncio
import time

import config
import message
import search


async def main():
    interval = config.INTERVAL_SEC
    shown_items = set()
    while True:
        items = search.search_items()
        if items:
            for item in items:
                if item['seq'] not in shown_items:
                    shown_items.add(item['seq'])
                    text = search.format_item(item)
                    await message.send_message(text)
        time.sleep(interval)


if __name__ == '__main__':
    asyncio.run(main())
