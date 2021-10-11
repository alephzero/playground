import a0
import time


def callback(pkt, done):
    print(f'Progress info: {pkt.payload.decode("utf-8")}')
    if done:
        print("Completed")


print("Waiting 1s for responses")
client = a0.PrpcClient("topic")
client.connect("client request", callback)
time.sleep(1)
print("Done!")
