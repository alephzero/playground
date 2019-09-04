#include <a0.h>

#include <chrono>
#include <iostream>
#include <system_error>
#include <thread>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::TopicManager tm(R"({
    "container": "stuff_doer"
  })");

  auto onrequest = [&](a0::RpcRequest req) {
    std::cout << "Request (id=" << req.pkt().id() << "): " << req.pkt().payload() << std::endl;
    req.reply("No path found. Try again later");
  };
  auto oncancel = [&](const std::string& id) {
    std::cout << "Cancel req: " << id << std::endl;
  };

  std::cout << "Listening for 60 sec" << std::endl;
  a0::RpcServer server(tm.rpc_server_topic("navigate"), onrequest, oncancel);
  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
