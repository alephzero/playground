import a0
import time


def callback(pkt):
    print(f'Recieved reply: {pkt.payload.decode("utf-8")}')


print("Waiting 1ms for response")
client = a0.RpcClient("topic")
client.send("client msg", callback)
time.sleep(0.001)
print("Done!")
