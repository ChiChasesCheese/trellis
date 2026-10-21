// EXPECTED TO FAIL under TSan (-fsanitize=thread): two threads, one plain int.
#include <cstdio>
#include <thread>
int main() {
    int counter = 0;
    std::thread a([&] { for (int i = 0; i < 100000; ++i) ++counter; });
    std::thread b([&] { for (int i = 0; i < 100000; ++i) ++counter; });
    a.join(); b.join();
    std::printf("%d\n", counter);
}
