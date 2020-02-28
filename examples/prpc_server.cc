#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager({
      .container = "vvv",
      .subscriber_aliases = {},
      .rpc_client_aliases = {},
      .prpc_client_aliases = {},
  });

  auto onconnect = [&](a0::PrpcConnection conn) {
    auto pkt_view = conn.pkt();
    std::cout << "Connection (id=" << pkt_view.id()
              << "): " << pkt_view.payload() << std::endl;
    for (int i = 0; i < 3; i++) {
      conn.send(std::string("msg ") + std::to_string(i), false);
      std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    conn.send("final msg", true);
  };

  std::cout << "Listening for 60 sec" << std::endl;
  a0::PrpcServer server("eee", onconnect, nullptr);
  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
