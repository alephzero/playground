#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager({
      .container = "xxx",
      .subscriber_aliases = {},
      .rpc_client_aliases = {},
      .prpc_client_aliases = {},
  });

  auto onrequest = [&](a0::RpcRequest req) {
    auto pkt_view = req.pkt();
    std::cout << "Request (id=" << pkt_view.id() << "): " << pkt_view.payload()
              << std::endl;
    req.reply("echo " + std::string(pkt_view.payload()));
  };

  std::cout << "Listening for 60 sec" << std::endl;
  a0::RpcServer server("ccc", onrequest, nullptr);
  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
