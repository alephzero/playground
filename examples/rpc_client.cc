#include <a0.h>

#include <chrono>
#include <iostream>
#include <system_error>
#include <thread>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager(R"({
    "container": "bar",
    "rpc_client_maps": {
      "drive_in_circles": {
        "container": "stuff_doer",
        "topic": "navigate"
      }
    }
  })");

  a0::RpcClient client("drive_in_circles");
  client.send("Please do!", [](a0::PacketView reply) {
    std::cout << "Recieved reply: " << reply.payload() << std::endl;
  });
  std::this_thread::sleep_for(std::chrono::milliseconds(1));
  std::cout << "Done!" << std::endl;
}
