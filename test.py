import time
import aiohttp
import asyncio

async def download_site(url, session):
    async with session.get(url) as res:
        print(f"content: {len(res.content)} from {url}")
        
async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks,return_exceptions=True)
  
if __name__ == '__main__':
    sites = [
         "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 100
    start = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start
    print(f'downloaded {len(sites)} in {duration} secs')