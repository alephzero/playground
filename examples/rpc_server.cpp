#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  auto onrequest = [&](a0::RpcRequest req) {
    auto pkt = req.pkt();
    std::cout << "Request (id=" << pkt.id() << "): " << pkt.payload()
              << std::endl;
    req.reply("echo " + std::string(pkt.payload()));
  };

  std::cout << "Listening for 60 sec" << std::endl;
  a0::RpcServer server("topic", onrequest, nullptr);
  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
