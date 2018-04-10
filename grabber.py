import os
import asyncio
from contextlib import closing
import aiohttp
import logging
import logging.config
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('grabber.conf')

DEST_PATH = config['DEFAULTS']['destination_path']

destination_path = os.path.join(DEST_PATH + '%03d.png')

s = 'http://game-a1.granbluefantasy.jp/assets/img/sp/assets/stamp/full/stamp%d.png'

async def retrieve_image(session, i):
    async with session.get(s % i) as response:
        if response.status == 200:
            content = await response.read()
            with open(destination_path % i, 'wb') as f:
                f.write(content)
        return response.status

async def download_multiple():
    count = 0
    async with aiohttp.ClientSession() as session:
        indexes = (i for i in range(1, 250))
        download_futures = [retrieve_image(session, idx) for idx in indexes]
        print('Results')
        for download_future in asyncio.as_completed(download_futures):
            if await download_future == 200:
                count += 1
        return count

def main():
    with closing(asyncio.get_event_loop()) as loop:
        result = loop.run_until_complete(download_multiple())
        print('finished: ', result)

main()
