import aiohttp
import asyncio
from pygtt import (
    PyGTT
)

loop = asyncio.get_event_loop()

async def test():
    async with aiohttp.ClientSession() as session:

        pygtt = PyGTT(session=session, stop_name="512",)
        stop = await pygtt.get_state()
        print (stop.name)
        for b in stop.bus_list:
            print (b.name)
            for t in b.time:
                print(t)
        


loop.run_until_complete(test())
loop.close()