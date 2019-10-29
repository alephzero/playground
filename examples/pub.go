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
  "container": "zzz"
}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenPublisherTopic("aaa")
	check(err)
	defer topic.Close()

	pub, err := a0.NewPublisher(topic)
	check(err)
	defer pub.Close()

	for i := 0; i < 10; i++ {
		payload := fmt.Sprintf("here (ts=%v)", i)
		fmt.Printf("publishing: %v\n", payload)
		pkt, err := a0.NewPacket(nil, []byte(payload))
		check(err)
		check(pub.Pub(pkt))
		time.Sleep(time.Second)
	}

	fmt.Println("Done!")
}
