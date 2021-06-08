import a0
import time


def callback(pkt_view, done):
    print(f'Progress info: {pkt_view.payload.decode("utf-8")}')
    if done:
        print('Completed')


print('Waiting 1s for responses')
client = a0.PrpcClient(a0.File('alephzero/example.prpc.a0'))
client.connect('client request', callback)
time.sleep(1)
print('Done!')
