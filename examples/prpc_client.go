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
		"container": "bar",
		"prpc_client_maps": {
			"drive_in_circles": {
				"container": "stuff_doer",
				"topic": "navigate"
			}
		}
	}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenPrpcClientTopic("drive_in_circles")
	check(err)
	defer topic.Close()

	client, err := a0.NewPrpcClient(topic)
	check(err)
	defer client.Close()

	var hdrs []a0.PacketHeader
	req, err := a0.NewPacket(hdrs, []byte("Please do!"))
	check(err)

	check(client.Connect(req, func(pkt a0.Packet, done bool) {
		payload, err := pkt.Payload()
		check(err)
		fmt.Printf("Recieved pkt: %v\n", string(payload))
		fmt.Printf("Done: %v\n", done)
	}))

	time.Sleep(time.Second)

	fmt.Println("Done!")
}

