package main

import (
	"fmt"
	a0 "github.com/alephzero/go"
	"log"
)

func check(err error) {
	if err != nil {
		log.Panicf("err: %v", err)
	}
}

func main() {
	tm, err := a0.NewTopicManager(`{
		"container": "controller",
		"subscriber_maps": {
			"where_am_I": {
				"container": "localizer",
				"topic": "location"
			}
		}
	}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenSubscriberTopic("where_am_I")
	check(err)
	defer topic.Close()

	sub, err := a0.NewSubscriberSync(topic, a0.INIT_MOST_RECENT, a0.ITER_NEWEST)
	check(err)
	defer sub.Close()

	for {
		hasNext, err := sub.HasNext()
		check(err)
		if !hasNext {
			break
		}
		pkt, err := sub.Next()
		check(err)

		payload, err := pkt.Payload()
		check(err)
		fmt.Printf("I am %v\n", string(payload))
	}

	fmt.Println("Done!")
}
