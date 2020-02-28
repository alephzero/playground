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
		Container: "zzz",
	}

	topic, err := tm.OpenPublisherTopic("aaa")
	check(err)
	defer topic.Close()

	pub, err := a0.NewPublisher(topic)
	check(err)
	defer pub.Close()

	for i := 0; i < 10; i++ {
		payload := fmt.Sprintf("here (ts=%v)", i)
		fmt.Printf("publishing: %v\n", payload)
		pkt := a0.NewPacket(nil, []byte(payload))
		check(pub.Pub(pkt))
		time.Sleep(time.Second)
	}

	fmt.Println("Done!")
}
