import requests
import time

def download_site(url, session):
    with session.get(url) as res:
        print(f"content: {len(res.content)} from {url}")

def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
          download_site(url, session)

if __name__ == '__main__':
    sites = [
         "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 100
    start = time.time()
    download_all_sites(sites)
    duration = time.time() - start
    print('downloaded {len(sites)} in {duration} secs')