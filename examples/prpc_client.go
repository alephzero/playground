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
		Container: "uuu",
		SubscriberAliases: map[string]a0.TopicAliasTarget{},
		RpcClientAliases: map[string]a0.TopicAliasTarget{},
		PrpcClientAliases: map[string]a0.TopicAliasTarget{
			"fff": a0.TopicAliasTarget{
				Container: "vvv",
				Topic: "eee",
			},
		},
	}

	topic, err := tm.OpenPrpcClientTopic("fff")
	check(err)
	defer topic.Close()

	client, err := a0.NewPrpcClient(topic)
	check(err)
	defer client.Close()

	req := a0.NewPacket(nil, []byte("client request"))

	fmt.Println("Waiting 1s for responses")

	check(client.Connect(req, func(pkt a0.Packet, done bool) {
		fmt.Printf("Progress info: %v\n", string(pkt.Payload))
		if done {
			fmt.Println("Completed")
		}
	}))

	time.Sleep(time.Second)

	fmt.Println("Done!")
}
