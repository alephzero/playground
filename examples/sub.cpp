#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  std::cout << "Listening for 60 sec" << std::endl;

  a0::Subscriber sub("topic", A0_INIT_AWAIT_NEW, A0_ITER_NEWEST,
                     [](a0::Packet pkt) {
                       std::cout << "Got: " << pkt.payload() << std::endl;
                     });

  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
