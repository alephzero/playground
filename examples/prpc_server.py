import a0
import json
import time

a0.InitGlobalTopicManager(a0.TopicManager(container = 'vvv'))


def onconnect(conn):
  pkt_view = conn.pkt
  print(f'Connection (id={pkt_view.id}): {pkt_view.payload}')
  for i in range(3):
    conn.send(f'msg {i}', False)
    time.sleep(0.1)
  conn.send('final msg', True)


print('Listening for 60 sec')
server = a0.PrpcServer('eee', onconnect, None)
time.sleep(60)
print('Done!')
