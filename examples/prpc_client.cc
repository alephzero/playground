#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager(R"({
    "container": "uuu",
    "prpc_client_maps": {
      "fff": {
        "container": "vvv",
        "topic": "eee"
      }
    }
  })");

  std::cout << "Waiting 1s for responses" << std::endl;
  a0::PrpcClient client("fff");
  client.connect("client request", [](a0::PacketView reply_view, bool done) {
    std::cout << "Recieved reply: " << reply_view.payload() << std::endl;
    if (done) {
      std::cout << "Completed!" << std::endl;
    }
  });
  std::this_thread::sleep_for(std::chrono::seconds(1));
  std::cout << "Done!" << std::endl;
}
