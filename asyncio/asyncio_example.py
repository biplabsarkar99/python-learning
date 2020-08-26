import aiohttp # Since requests is a blocking module, it wait for response.
from timer import timer
import asyncio

URL = 'https://httpbin.org/uuid'

'''
With async we make the function as co-routine
a co-routine, can wait for its completion while
other co-routine is executed.
'''
async def fetch (session, url):
    async with session.get(url) as response:
        json_response = await response.json()
        print (json_response['uuid'])

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        # for _ in range(100):
        #     fetch(session, URL)
        tasks = [fetch(session, URL) for _ in range(100)]
        await asyncio.gather(*tasks) #Gather bunch on coroutines, and executes them togather.

@timer(1,1)
def func():
    asyncio.run(main()) #Run the main cou routine