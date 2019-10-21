import a0
import time

a0.InitGlobalTopicManager('''{
    "container": "stuff_doer"
}''')


def onconnect(conn):
    print('Connection (id={}):'.format(conn.pkt.id), conn.pkt.payload)
    for i in range(3):
        conn.send(f'msg {i}', False)
        time.sleep(0.1)
    conn.send('final msg', True)


def oncancel(id):
    print('Cancel req:', id)


print('Listening for 60 sec')
server = a0.PrpcServer('navigate', onconnect, oncancel)
time.sleep(60)
print('Done!')
