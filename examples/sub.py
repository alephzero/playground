import a0
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


def callback(pkt_view):
  print(f'Got: {pkt_view.payload.decode("utf-8")}')


print('Listening for 60 sec')
sub = a0.Subscriber('bbb', a0.INIT_AWAIT_NEW, a0.ITER_NEWEST, callback)
time.sleep(60)
print('Done!')
