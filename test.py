import requests
import time
import threading
import concurrent.futures


thread_local = threading.local() #??

def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def download_site(url):
    session = get_session()
    with session.get(url) as res:
        print(f"content: {len(res.content)} from {url}")

def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exc:
        exc.map(download_site, sites)
  
if __name__ == '__main__':
    sites = [
         "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 100
    start = time.time()
    download_all_sites(sites)
    duration = time.time() - start
    print(f'downloaded {len(sites)} in {duration} secs')