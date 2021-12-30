#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::SubscriberSync sub("topic", a0::INIT_OLDEST);
  while (sub.can_read()) {
    a0::Packet pkt = sub.read();
    std::cout << pkt.payload() << std::endl;
  }
}
