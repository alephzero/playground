import a0
import time

tm = a0.TopicManager('''{
    "container": "Endor",
    "subscriber_maps": {
        "where_am_I": {
            "container": "localizer",
            "topic": "location"
        }
    }
}''')


def callback(pkt):
    print('I am', pkt.payload)


print('Listening for 60 sec')
sub = a0.Subscriber(
    tm.subscriber_topic('where_am_I'),
    a0.INIT_AWAIT_NEW,
    a0.ITER_NEWEST,
    callback)
time.sleep(60)
print('Done!')
