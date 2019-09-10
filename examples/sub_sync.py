import a0

a0.InitGlobalTopicManager('''{
    "container": "controller",
    "subscriber_maps": {
        "where_am_I": {
            "container": "localizer",
            "topic": "location"
        }
    }
}''')

sub = a0.SubscriberSync(
    'where_am_I',
    a0.INIT_OLDEST,
    a0.ITER_NEXT)
print('Starting iteration')
while sub.has_next():
    print('I am', sub.next().payload)
print('Done!')
