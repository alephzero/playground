import a0
import asyncio


async def main():
    async for pkt in a0.aio_sub("topic"):
        print(pkt.payload)


print("Listening for 60 sec")
try:
    asyncio.run(asyncio.wait_for(main(), timeout=60.0))
except asyncio.TimeoutError:
    pass
print("Done!")
