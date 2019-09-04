import a0
import time

tm = a0.TopicManager('''{
    "container": "localizer"
}''')

p = a0.Publisher(tm.publisher_topic('location'))
for i in range(10):
	payload = 'here (ts={})'.format(i)
	print('publishing:', payload)
	p.pub(a0.Packet([], payload))
	time.sleep(1)

print('Done!')
