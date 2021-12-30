import a0

sub = a0.SubscriberSync("topic", a0.INIT_OLDEST)
while sub.can_read():
    pkt = sub.read()
    print(pkt.payload)
