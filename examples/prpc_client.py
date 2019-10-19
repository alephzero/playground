import a0
import time

a0.InitGlobalTopicManager('''{
    "container": "bar",
    "prpc_client_maps": {
        "drive_in_circles": {
            "container": "stuff_doer",
            "topic": "navigate"
        }
    }
}''')

client = a0.RpcClient('drive_in_circles')


def callback(pkt, done):
    print('Progress info:', pkt.payload)
    if done:
        print('Completed')


print('Awaiting for 1 sec')
client.send('Please do!', callback)
time.sleep(1)
print('Done!')
