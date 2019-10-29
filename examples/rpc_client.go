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
  "container": "www",
  "rpc_client_maps": {
    "ddd": {
      "container": "xxx",
      "topic": "ccc"
    }
  }
}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenRpcClientTopic("ddd")
	check(err)
	defer topic.Close()

	client, err := a0.NewRpcClient(topic)
	check(err)
	defer client.Close()

	req, err := a0.NewPacket(nil, []byte("client msg"))
	check(err)

	fmt.Println("Waiting 1ms for response")

	check(client.Send(req, func(reply a0.Packet) {
		payload, err := reply.Payload()
		check(err)
		fmt.Printf("Recieved reply: %v\n", string(payload))
	}))

	time.Sleep(time.Millisecond)

	fmt.Println("Done!")
}
