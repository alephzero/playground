#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager(R"({
    "container": "yyy",
    "subscriber_maps": {
      "bbb": {
        "container": "zzz",
        "topic": "aaa"
      }
    }
  })");

  std::cout << "Listening for 60 sec" << std::endl;

  a0::Subscriber sub("bbb", A0_INIT_AWAIT_NEW, A0_ITER_NEWEST,
                     [](a0::PacketView pkt_view) {
                       std::cout << "Got: " << pkt_view.payload() << std::endl;
                     });

  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
