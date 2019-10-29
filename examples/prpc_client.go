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
  "container": "uuu",
  "prpc_client_maps": {
    "fff": {
      "container": "vvv",
      "topic": "eee"
    }
  }
}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenPrpcClientTopic("fff")
	check(err)
	defer topic.Close()

	client, err := a0.NewPrpcClient(topic)
	check(err)
	defer client.Close()

	req, err := a0.NewPacket(nil, []byte("client request"))
	check(err)

	fmt.Println("Waiting 1s for responses")

	check(client.Connect(req, func(pkt a0.Packet, done bool) {
		payload, err := pkt.Payload()
		check(err)
		fmt.Printf("Progress info: %v\n", string(payload))
		if done {
			fmt.Println("Completed")
		}
	}))

	time.Sleep(time.Second)

	fmt.Println("Done!")
}
