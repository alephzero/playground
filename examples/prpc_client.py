import a0
import json
import time

a0.InitGlobalTopicManager(
    json.dumps({
        'container': 'uuu',
        'prpc_client_maps': {
            'fff': {
                'container': 'vvv',
                'topic': 'eee'
            }
        },
    }))

client = a0.PrpcClient('fff')


def callback(pkt_view, done):
  print(f'Progress info: {pkt_view.payload.decode("utf-8")}')
  if done:
    print('Completed')


print('Waiting 1s for responses')
client.connect('client request', callback)
time.sleep(1)
print('Done!')
