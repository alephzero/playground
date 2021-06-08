import a0
import time


def callback(pkt_view):
    print(f'Recieved reply: {pkt_view.payload.decode("utf-8")}')


print('Waiting 1ms for response')
client = a0.RpcClient(a0.File('alephzero/example.rpc.a0'))
client.send('client msg', callback)
time.sleep(0.001)
print('Done!')
