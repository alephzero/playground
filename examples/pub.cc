#include <a0.h>

#include <chrono>
#include <iostream>
#include <system_error>
#include <thread>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::TopicManager tm(R"({
        "container": "localizer"
	})");

  a0::Publisher p(tm.publisher_topic("location"));

  for (int i = 0; i < 10; i++) {
    std::string payload = "here (ts=" + std::to_string(i) + ")";
    std::cout << "publishing: " << payload << std::endl;
    p.pub(payload);
    std::this_thread::sleep_for(std::chrono::seconds(1));
  }

  std::cout << "Done!" << std::endl;
}
