import a0
import json
import time

a0.InitGlobalTopicManager(json.dumps({'container': 'xxx'}))


def onrequest(req):
  pkt_view = req.pkt
  payload = pkt_view.payload.decode('utf-8')
  print(f'Request (id={pkt_view.id}): {payload}')
  req.reply(f'echo {payload}')


print('Listening for 60 sec')
server = a0.RpcServer('ccc', onrequest, None)
time.sleep(60)
print('Done!')
