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
		"rpc_client_maps": {
			"drive_in_circles": {
				"container": "stuff_doer",
				"topic": "navigate"
			}
		}
	}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenRpcClientTopic("drive_in_circles")
	check(err)
	defer topic.Close()

	client, err := a0.NewRpcClient(topic)
	check(err)
	defer client.Close()

	var hdrs []a0.PacketHeader
	req, err := a0.NewPacket(hdrs, []byte("Please do!"))
	check(err)

	check(client.Send(req, func(reply a0.Packet) {
		payload, err := reply.Payload()
		check(err)
		fmt.Printf("Recieved reply: %v\n", string(payload))
	}))

	time.Sleep(time.Second)

	fmt.Println("Done!")
}
