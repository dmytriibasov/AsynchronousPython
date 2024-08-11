import sys
import asyncio
import aiohttp
import aiofiles
from urllib.parse import urlparse


async def generate_filepath(url: str):
    parsed_url = urlparse(url)
    filename = parsed_url.hostname.replace(".", "_") + parsed_url.path.replace("/", "_")
    new_filename = filename if filename.endswith(".html") else f"{filename}.html"
    return f"{new_filename}"


async def fetch_data(session, url):
    async with session.get(url) as response:
        filepath = await generate_filepath(url)
        async with aiofiles.open(filepath, 'wb') as fd:
            async for chunk in response.content.iter_chunked(100):
                await fd.write(chunk)


async def process_url(url):
    if url:
        async with aiohttp.ClientSession() as session:
            try:
                async with asyncio.timeout(10):
                    await fetch_data(session, url)
            except asyncio.TimeoutError as e:
                print(f'Timeout Error - {url}')
            except Exception as e:
                print(f'{e} - {url}')


async def read_file(filepath):
    tasks = []
    async with aiofiles.open(filepath, "r") as file:
        async for url in file:
            if url:
                tasks.append(process_url(url))
    return tasks


async def main(filepath):
    tasks = await read_file(filepath)
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    filepath = sys.argv[-1]
    asyncio.run(main(filepath))
