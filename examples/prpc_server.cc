#include <a0.h>

#include <chrono>
#include <iostream>
#include <system_error>
#include <thread>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager(R"({
    "container": "stuff_doer"
  })");

  auto onconnect = [&](a0::PrpcConnection conn) {
    std::cout << "Request (id=" << req.pkt().id() << "): " << conn.pkt().payload() << std::endl;
    for (int i = 0; i < 3; i++) {
        conn.send(std::string("msg ") + std::to_string(i), false);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    conn.send("final msg", true);
  };
  auto oncancel = [&](const std::string& id) {
    std::cout << "Cancel req: " << id << std::endl;
  };

  std::cout << "Listening for 60 sec" << std::endl;
  a0::RpcServer server("navigate", onrequest, oncancel);
  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
