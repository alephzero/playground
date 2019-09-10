#include <a0.h>

#include <chrono>
#include <iostream>
#include <system_error>
#include <thread>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager(R"({
    "container": "controller",
    "subscriber_maps": {
      "where_am_I": {
        "container": "localizer",
        "topic": "location"
      }
    }
  })");

  std::cout << "Listening for 60 sec" << std::endl;

  a0::Subscriber sub("where_am_I",
                     A0_INIT_AWAIT_NEW,
                     A0_ITER_NEWEST,
                     [](a0::PacketView pkt) {
                       std::cout << "I am " << pkt.payload() << std::endl;
                     });

  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
