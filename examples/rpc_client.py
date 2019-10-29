import a0
import json
import time

a0.InitGlobalTopicManager(
    json.dumps({
        'container': 'www',
        'rpc_client_maps': {
            'ddd': {
                'container': 'xxx',
                'topic': 'ccc'
            }
        },
    }))

client = a0.RpcClient('ddd')


def callback(pkt_view):
  print(f'Recieved reply: {pkt_view.payload.decode("utf-8")}')


print('Waiting 1ms for response')
client.send('client msg', callback)
time.sleep(0.001)
print('Done!')
