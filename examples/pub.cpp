#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::Publisher p("topic");

  for (int i = 0; i < 10; i++) {
    std::string payload = "here (ts=" + std::to_string(i) + ")";
    std::cout << "publishing: " << payload << std::endl;
    p.pub(payload);
    std::this_thread::sleep_for(std::chrono::seconds(1));
  }

  std::cout << "Done!" << std::endl;
}
