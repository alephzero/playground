import a0
import asyncio
import json
import time

a0.InitGlobalTopicManager(a0.TopicManager(
    container = 'www',
    rpc_client_aliases = {
        'ddd': a0.TopicAliasTarget(
            container = 'xxx',
            topic = 'ccc',
        )
    }
))


async def main():
    client = a0.AioRpcClient('ddd')
    reply = await client.send('client msg')
    print(f'Recieved reply: {reply.payload.decode("utf-8")}')


asyncio.run(main())
print('Done!')
