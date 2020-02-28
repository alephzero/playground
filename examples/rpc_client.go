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
		Container: "www",
		RpcClientAliases: map[string]a0.TopicAliasTarget{
			"ddd": {
				Container: "xxx",
				Topic: "ccc",
			},
		},
	}

	topic, err := tm.OpenRpcClientTopic("ddd")
	check(err)
	defer topic.Close()

	client, err := a0.NewRpcClient(topic)
	check(err)
	defer client.Close()

	req := a0.NewPacket(nil, []byte("client msg"))

	fmt.Println("Waiting 1ms for response")

	check(client.Send(req, func(reply a0.Packet) {
		fmt.Printf("Recieved reply: %v\n", string(reply.Payload))
	}))

	time.Sleep(time.Millisecond)

	fmt.Println("Done!")
}
