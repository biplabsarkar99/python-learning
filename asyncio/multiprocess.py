import requests
from timer import timer
from multiprocessing import Pool

URL = 'https://httpbin.org/uuid'

def fetch (session, url):
    with session.get(url) as response:
        print(response.json()['uuid'])

@timer(1,1)
def main():
    # with requests.Session() as session:
    #     for _ in range(100):
    #         fetch(session, URL)
    with Pool() as pool:
        with requests.Session() as session:
            pool.starmap(fetch, [(session, URL) for _ in range(100)])