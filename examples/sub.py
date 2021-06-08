import a0
import time


def callback(pkt_view):
    print(f'Got: {pkt_view.payload.decode("utf-8")}')


print('Listening for 60 sec')
topic = a0.File('alephzero/example.pubsub.a0')
sub = a0.Subscriber(topic, a0.INIT_AWAIT_NEW, a0.ITER_NEWEST, callback)
time.sleep(60)
print('Done!')
