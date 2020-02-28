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
		Container: "vvv",
	}

	topic, err := tm.OpenPrpcServerTopic("eee")
	check(err)
	defer topic.Close()

	onconnect := func(conn a0.PrpcConnection) {
		pkt := conn.Packet()
		fmt.Printf("Connection (id=%v): %v\n", pkt.ID(), string(pkt.Payload))

		for i := 0; i < 3; i++ {
			pkt = a0.NewPacket(nil, []byte(fmt.Sprintf("msg %v", i)))
			check(conn.Send(pkt, false))
		}

		pkt = a0.NewPacket(nil, []byte("final msg"))
		check(conn.Send(pkt, true))
	}

	fmt.Println("Listening for 60 sec")

	server, err := a0.NewPrpcServer(topic, onconnect, nil)
	check(err)
	defer server.Close()

	time.Sleep(60 * time.Second)

	fmt.Println("Done!")
}
