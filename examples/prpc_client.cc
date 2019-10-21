#include <a0.h>

#include <chrono>
#include <iostream>
#include <system_error>
#include <thread>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager(R"({
    "container": "bar",
    "prpc_client_maps": {
      "drive_in_circles": {
        "container": "stuff_doer",
        "topic": "navigate"
      }
    }
  })");

  a0::PrpcClient client("drive_in_circles");
  client.connect("Please do!", [](a0::PacketView reply, bool done) {
    std::cout << "Recieved reply: " << reply.payload() << std::endl;
    if (done) {
      std::cout << "Completed!" << std::endl;
    }
  });
  std::this_thread::sleep_for(std::chrono::seconds(1));
  std::cout << "Done!" << std::endl;
}
