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
	tm, err := a0.NewTopicManagerFromJSON(`{
        "container": "localizer"
    }`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenPublisherTopic("location")
	check(err)
	defer topic.Close()

	pub, err := a0.NewPublisher(topic)
	check(err)
	defer pub.Close()

	for i := 0; i < 10; i++ {
		var hdrs []a0.PacketHeader
		pkt, err := a0.NewPacket(hdrs, []byte(fmt.Sprintf("here (ts=%v)", i)))
		check(err)
		check(pub.Pub(pkt))
		time.Sleep(time.Second)
	}

	fmt.Println("Done!")
}
