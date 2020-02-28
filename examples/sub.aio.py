import a0
import asyncio
import json
import time

a0.InitGlobalTopicManager(a0.TopicManager(
    container = 'yyy',
    subscriber_aliases = {
        'bbb': a0.TopicAliasTarget(
            container = 'zzz',
            topic = 'aaa'
        )
    }
))


async def main():
    async for pkt in a0.aio_sub('bbb', a0.INIT_AWAIT_NEW, a0.ITER_NEWEST):
        print(f'Got: {pkt.payload.decode("utf-8")}')


print('Listening for 60 sec')
try:
    asyncio.run(asyncio.wait_for(main(), timeout=60.0))
except asyncio.TimeoutError:
    pass
print('Done!')
