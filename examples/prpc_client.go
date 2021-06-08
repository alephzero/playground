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
	topic, err := a0.FileOpen("alephzero/example.prpc.a0", nil)
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
