#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  std::cout << "Listening for 60 sec" << std::endl;

  a0::Subscriber sub("topic",
                     [](a0::Packet pkt) {
                       std::cout << pkt.payload() << std::endl;
                     });

  std::this_thread::sleep_for(std::chrono::seconds(60));
  std::cout << "Done!" << std::endl;
}
