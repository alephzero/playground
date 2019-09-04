import a0
import time

tm = a0.TopicManager('''{
    "container": "stuff_doer"
}''')

def onrequest(req):
	print('Request (id={}):'.format(req.pkt.id), req.pkt.payload)
	req.reply('No path found. Try again later')

def oncancel(id):
	print('Cancel req:', id)

print('Listening for 60 sec')
server = a0.RpcServer(tm.rpc_server_topic('navigate'), onrequest, oncancel)
time.sleep(60)
print('Done!')
