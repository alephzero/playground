import a0
import json
import time

a0.InitGlobalTopicManager(
    json.dumps({
        'container': 'yyy',
        'subscriber_maps': {
            'bbb': {
                'container': 'zzz',
                'topic': 'aaa'
            }
        }
    }))


def callback(pkt_view):
  print(f'Got: {pkt_view.payload.decode("utf-8")}')


print('Listening for 60 sec')
sub = a0.Subscriber('bbb', a0.INIT_AWAIT_NEW, a0.ITER_NEWEST, callback)
time.sleep(60)
print('Done!')
