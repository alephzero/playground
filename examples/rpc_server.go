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

	topic, err := tm.OpenRpcServerTopic("navigate")
	check(err)
	defer topic.Close()

	onrequest := func(req a0.RpcRequest) {
		payload, err := req.Packet().Payload()
		check(err)
		id, err := req.Packet().Id()
		check(err)
		fmt.Printf("Request (id=%v): %v\n", id, string(payload))

		var hdrs []a0.PacketHeader
		replyPkt, err := a0.NewPacket(hdrs, []byte("No path found. Try again later"))
		check(err)
		check(req.Reply(replyPkt))
	}
	oncancel := func(id string) {
		fmt.Printf("Cancel req: %v\n", id)
	}
	server, err := a0.NewRpcServer(topic, onrequest, oncancel)
	check(err)
	defer server.Close()

	time.Sleep(60 * time.Second)

	fmt.Println("Done!")
}
