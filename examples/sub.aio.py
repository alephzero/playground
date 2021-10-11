import a0
import asyncio


async def main():
    async for pkt in a0.aio_sub("topic", a0.INIT_AWAIT_NEW, a0.ITER_NEWEST):
        print(f'Got: {pkt.payload.decode("utf-8")}')


print("Listening for 60 sec")
try:
    asyncio.run(asyncio.wait_for(main(), timeout=60.0))
except asyncio.TimeoutError:
    pass
print("Done!")
