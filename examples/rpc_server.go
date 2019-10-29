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
  "container": "xxx"
}`)
	check(err)
	defer tm.Close()

	topic, err := tm.OpenRpcServerTopic("ccc")
	check(err)
	defer topic.Close()

	onrequest := func(req a0.RpcRequest) {
		payload, err := req.Packet().Payload()
		check(err)
		id, err := req.Packet().Id()
		check(err)
		fmt.Printf("Request (id=%v): %v\n", id, string(payload))

		replyPkt, err := a0.NewPacket(nil, []byte(fmt.Sprintf("echo %v", string(payload))))
		check(err)
		check(req.Reply(replyPkt))
	}

	fmt.Println("Listening for 60 sec")

	server, err := a0.NewRpcServer(topic, onrequest, nil)
	check(err)
	defer server.Close()

	time.Sleep(60 * time.Second)

	fmt.Println("Done!")
}
