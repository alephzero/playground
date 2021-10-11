import a0
import time


def onrequest(req):
    pkt = req.pkt
    payload = pkt.payload.decode("utf-8")
    print(f"Request (id={pkt.id}): {payload}")
    req.reply(f"echo {payload}")


print("Listening for 60 sec")
server = a0.RpcServer("topic", onrequest, None)
time.sleep(60)
print("Done!")
