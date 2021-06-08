#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  auto onrequest = [&](a0::RpcRequest req) {
    auto pkt_view = req.pkt();
    std::cout << "Request (id=" << pkt_view.id() << "): " << pkt_view.payload()
              << std::endl;
    req.reply("echo " + std::string(pkt_view.payload()));
  };

  std::cout << "Listening for 60 sec" << std::endl;
  a0::File topic("alephzero/example.rpc.a0");
  a0::RpcServer server(topic, onrequest, nullptr);
  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
