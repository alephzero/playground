#include <a0.h>
#include <iostream>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::InitGlobalTopicManager({
      .container = "www",
      .subscriber_aliases = {},
      .rpc_client_aliases = {
        {"ddd", {
          .container = "xxx",
          .topic = "ccc",
        }}
      },
      .prpc_client_aliases = {},
  });

  // // Callback version:
  // a0::RpcClient client("ddd");
  // client.send("client msg", [](a0::PacketView reply_view) {
  //   std::cout << "Recieved reply: " << reply_view.payload() << std::endl;
  // });
  // std::this_thread::sleep_for(std::chrono::milliseconds(1));

  a0::RpcClient client("ddd");
  auto reply_fut = client.send("client msg");
  std::cout << "Recieved reply: " << reply_fut.get().payload() << std::endl;
  std::cout << "Done!" << std::endl;
}
