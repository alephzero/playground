package main

import (
	"fmt"
	a0 "github.com/alephzero/go"
	"log"
	"time"
)

func check(err error) {
	if err != nil {
		log.Panicf("err: %v", err)
	}
}

func main() {
	tm, err := a0.NewTopicManager(`{
  "container": "yyy",
  "subscriber_maps": {
    "bbb": {
      "container": "zzz",
      "topic": "aaa"
    }
  }
}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenSubscriberTopic("bbb")
	check(err)
	defer topic.Close()

	fmt.Println("Listening for 60 sec")

	sub, err := a0.NewSubscriber(topic, a0.INIT_AWAIT_NEW, a0.ITER_NEWEST, func(pkt a0.Packet) {
		payload, err := pkt.Payload()
		check(err)
		fmt.Printf("Got: %v\n", string(payload))
	})
	check(err)
	defer sub.Close()

	time.Sleep(60 * time.Second)

	fmt.Println("Done!")
}
