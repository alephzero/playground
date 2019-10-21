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
		"container": "stuff_doer"
	}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenPrpcServerTopic("navigate")
	check(err)
	defer topic.Close()

	onconnect := func(conn a0.PrpcConnection) {
		payload, err := conn.Packet().Payload()
		check(err)
		id, err := conn.Packet().Id()
		check(err)
		fmt.Printf("Request (id=%v): %v\n", id, string(payload))

		var hdrs []a0.PacketHeader
		pkt0, err := a0.NewPacket(hdrs, []byte("msg 0"))
		check(err)
		check(conn.Send(pkt0, false))

		pkt1, err := a0.NewPacket(hdrs, []byte("msg 1"))
		check(err)
		check(conn.Send(pkt1, true))
	}
	oncancel := func(id string) {
		fmt.Printf("Cancel req: %v\n", id)
	}
	server, err := a0.NewPrpcServer(topic, onconnect, oncancel)
	check(err)
	defer server.Close()

	time.Sleep(60 * time.Second)

	fmt.Println("Done!")
}

