#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  // // Callback version:
  // a0::RpcClient client("topic");
  // client.send("client msg", [](a0::Packet reply) {
  //   std::cout << "Recieved reply: " << reply.payload() << std::endl;
  // });
  // std::this_thread::sleep_for(std::chrono::milliseconds(1));

  a0::RpcClient client("topic");
  auto reply_fut = client.send("client msg");
  std::cout << "Recieved reply: " << reply_fut.get().payload() << std::endl;
  std::cout << "Done!" << std::endl;
}
