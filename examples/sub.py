import a0
import time

print("Listening for 60 sec")
sub = a0.Subscriber("topic", lambda pkt: print(pkt.payload))
time.sleep(60)
print("Done!")
