import a0
import asyncio


async def main():
    client = a0.AioRpcClient(a0.File('alephzero/example.rpc.a0'))
    reply = await client.send('client msg')
    print(f'Recieved reply: {reply.payload.decode("utf-8")}')


asyncio.run(main())
print('Done!')
