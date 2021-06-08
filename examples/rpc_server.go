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
	topic, err := a0.FileOpen("alephzero/example.rpc.a0", nil)
	check(err)
	defer topic.Close()

	onrequest := func(req a0.RpcRequest) {
		pkt := req.Packet()
		fmt.Printf("Request (id=%v): %v\n", pkt.ID(), string(pkt.Payload))

		replyPkt := a0.NewPacket(nil, []byte(fmt.Sprintf("echo %v", string(pkt.Payload))))
		check(req.Reply(replyPkt))
	}

	fmt.Println("Listening for 60 sec")

	server, err := a0.NewRpcServer(topic, onrequest, nil)
	check(err)
	defer server.Close()

	time.Sleep(60 * time.Second)

	fmt.Println("Done!")
}
