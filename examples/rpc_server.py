import a0
import time


def onrequest(req):
    pkt_view = req.pkt
    payload = pkt_view.payload.decode('utf-8')
    print(f'Request (id={pkt_view.id}): {payload}')
    req.reply(f'echo {payload}')


print('Listening for 60 sec')
topic = a0.File('alephzero/example.rpc.a0')
server = a0.RpcServer(topic, onrequest, None)
time.sleep(60)
print('Done!')
