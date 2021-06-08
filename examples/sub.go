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
	topic, err := a0.FileOpen("alephzero/example.pubsub.a0", nil)
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
