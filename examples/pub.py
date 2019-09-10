import a0
import time

a0.InitGlobalTopicManager('''{
    "container": "localizer"
}''')

p = a0.Publisher('location')
for i in range(10):
    payload = 'here (ts={})'.format(i)
    print('publishing:', payload)
    p.pub(payload)
    time.sleep(1)

print('Done!')
