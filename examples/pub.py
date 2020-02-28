import a0
import json
import time

a0.InitGlobalTopicManager(a0.TopicManager(container = 'zzz'))

p = a0.Publisher('aaa')
for i in range(10):
  payload = f'here (ts={i})'
  print(f'publishing: {payload}')
  p.pub(payload)
  time.sleep(1)

print('Done!')
