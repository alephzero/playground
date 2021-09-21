import a0
import time


def onconnect(conn):
    pkt = conn.pkt
    print(f"Connection (id={pkt.id}): {pkt.payload}")
    for i in range(3):
        conn.send(f"msg {i}", False)
        time.sleep(0.1)
    conn.send("final msg", True)


print("Listening for 60 sec")
server = a0.PrpcServer("topic", onconnect, None)
time.sleep(60)
print("Done!")
