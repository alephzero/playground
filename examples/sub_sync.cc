#include <a0.h>

#include <chrono>
#include <iostream>
#include <system_error>
#include <thread>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::TopicManager tm(R"({
		"container": "controller",
		"subscriber_maps": {
			"where_am_I": {
				"container": "localizer",
				"topic": "location"
			}
		}
  })");

  a0::SubscriberSync sub(tm.subscriber_topic("where_am_I"), A0_INIT_OLDEST, A0_ITER_NEXT);

  while (sub.has_next()) {
    auto pkt = sub.next();
    std::cout << "I am " << pkt.payload() << std::endl;
  }

  std::cout << "Done!" << std::endl;
}
