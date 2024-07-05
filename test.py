import requests
import multiprocessing
import time

session = None

def set_global_session():
    global session
    if not session:
        session = requests.Session()

def download_site(url):
    with session.get(url) as res:
        print(f"content: {len(res.content)} from {url}")

def download_all_sites(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites)

      
if __name__ == '__main__':
    sites = [
         "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 100
    start = time.time()
    download_all_sites(sites)
    duration = time.time() - start
    print(f'downloaded {len(sites)} in {duration} secs')