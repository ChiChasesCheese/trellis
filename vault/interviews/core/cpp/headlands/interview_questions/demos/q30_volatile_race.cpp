// volatile is not atomic: updates are lost. (This is a data race, i.e. undefined behaviour; run it only to see the symptom.)
#include <atomic>
#include <cstdio>
#include <mutex>
#include <thread>
#include <vector>

int main() {
    volatile int vcount = 0;
    std::atomic<int> acount{0};
    int mcount = 0; std::mutex m;
    std::vector<std::thread> ts;
    for (int t = 0; t < 4; ++t)
        ts.emplace_back([&] {
            for (int i = 0; i < 500000; ++i) {
                vcount = vcount + 1;                           // read, add, write: three steps
                acount.fetch_add(1);
                std::lock_guard g(m); ++mcount;
            }
        });
    for (auto& t : ts) t.join();
    std::printf("expected 2000000\n");
    int seen = vcount;
    std::printf("volatile int : %d%s\n", seen, seen == 2000000 ? " (lucky run)" : "  <- lost updates");
    std::printf("atomic<int>  : %d\n", acount.load());
    std::printf("mutex + int  : %d\n", mcount);
}
