import a0
import time


def callback(pkt):
    print(f'Got: {pkt.payload.decode("utf-8")}')


print("Listening for 60 sec")
sub = a0.Subscriber("topic", a0.INIT_AWAIT_NEW, a0.ITER_NEWEST, callback)
time.sleep(60)
print("Done!")
