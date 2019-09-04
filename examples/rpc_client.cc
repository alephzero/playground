#include <a0.h>
#include <chrono>
#include <iostream>
#include <system_error>
#include <thread>

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);

    a0::TopicManager tm(R"({
		"container": "bar",
		"rpc_client_maps": {
			"drive_in_circles": {
				"container": "stuff_doer",
				"topic": "navigate"
			}
		}
	})");

	a0::RpcClient client(tm.rpc_client_topic("drive_in_circles"));
	client.send(
		"Please do!",
		[](const a0::Packet& reply) {
			std::cout << "Recieved reply: " << reply.payload() << std::endl;
		}
	);
	std::this_thread::sleep_for(std::chrono::milliseconds(1));
	std::cout << "Done!" << std::endl;
}
