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
	tm := a0.TopicManager{
		Container: "yyy",
		SubscriberAliases: map[string]a0.TopicAliasTarget{
			"bbb": a0.TopicAliasTarget{
				Container: "zzz",
				Topic: "aaa",
			},
		},
		RpcClientAliases: map[string]a0.TopicAliasTarget{},
		PrpcClientAliases: map[string]a0.TopicAliasTarget{},
	}

	topic, err := tm.OpenSubscriberTopic("bbb")
	check(err)
	defer topic.Close()

	fmt.Println("Listening for 60 sec")

	sub, err := a0.NewSubscriber(topic, a0.INIT_AWAIT_NEW, a0.ITER_NEWEST, func(pkt a0.Packet) {
		fmt.Printf("Got: %v\n", string(pkt.Payload))
	})
	check(err)
	defer sub.Close()

	time.Sleep(60 * time.Second)

	fmt.Println("Done!")
}
