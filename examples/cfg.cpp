#include <a0.h>
#include <iostream>
#include <nlohmann/json.hpp>

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  a0::Cfg cfg("state");
  
  cfg.write(nlohmann::json{
      {"a", 1},
      {"b", {{"c", "Hello, World!"}}},
  });
  
  auto a = cfg.var<int>("/a");
  auto full_cfg = cfg.var<nlohmann::json>();

  std::cout << "original:\n  a=" << *a << std::endl;
  
  cfg.mergepatch({{"a", 2}});
  
  std::cout << "changed, but not updated:\n  a="
            << *a << std::endl;

  cfg.update_var();
  
  std::cout << "updated:\n  a="
            << *a << std::endl;
            
  std::cout << "\nfull cfg:\n"
            << full_cfg->dump(2) << std::endl;
}
