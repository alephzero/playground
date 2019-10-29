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
  "container": "vvv"
}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenPrpcServerTopic("eee")
	check(err)
	defer topic.Close()

	onconnect := func(conn a0.PrpcConnection) {
		payload, err := conn.Packet().Payload()
		check(err)
		id, err := conn.Packet().Id()
		check(err)
		fmt.Printf("Connection (id=%v): %v\n", id, string(payload))

		for i := 0; i < 3; i++ {
			pkt, err := a0.NewPacket(nil, []byte(fmt.Sprintf("msg %v", i)))
			check(err)
			check(conn.Send(pkt, false))
		}

		pkt, err := a0.NewPacket(nil, []byte("final msg"))
		check(err)
		check(conn.Send(pkt, true))
	}

	fmt.Println("Listening for 60 sec")

	server, err := a0.NewPrpcServer(topic, onconnect, nil)
	check(err)
	defer server.Close()

	time.Sleep(60 * time.Second)

	fmt.Println("Done!")
}
