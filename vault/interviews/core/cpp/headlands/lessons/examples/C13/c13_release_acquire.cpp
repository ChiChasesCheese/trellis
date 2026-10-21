// C13: release/acquire: publishing data from one thread to another, and a spinlock built from one atomic flag.
#include <atomic>
#include <cassert>
#include <iostream>
#include <thread>
#include <vector>

// [[snip:publish]]
struct Msg { int a = 0; int b = 0; };
Msg msg;                                   // plain, non-atomic data
std::atomic<bool> ready{false};

void producer() {
    msg.a = 1; msg.b = 2;                                   // (1) write the data
    ready.store(true, std::memory_order_release);           // (2) publish: everything before this is visible to an acquirer
}
void consumer() {
    while (!ready.load(std::memory_order_acquire)) { }      // (3) acquire pairs with the release store
    assert(msg.a == 1 && msg.b == 2);                       // (4) guaranteed to see the writes from (1)
    std::cout << "consumer saw " << msg.a << "," << msg.b << "\n";
}
// [[/snip]]

// [[snip:spin]]
class SpinLock {
    std::atomic_flag f_ = ATOMIC_FLAG_INIT;
public:
    void lock() { while (f_.test_and_set(std::memory_order_acquire)) { std::this_thread::yield(); } }   // acquire on entry
    void unlock() { f_.clear(std::memory_order_release); }                                              // release on exit
};
// [[/snip]]

int main() {
    std::thread c(consumer), p(producer);
    c.join(); p.join();

    SpinLock sl;
    long shared = 0;                                       // protected by the spinlock: no atomics needed
    std::vector<std::thread> ts;
    for (int t = 0; t < 4; ++t) ts.emplace_back([&] { for (int i = 0; i < 50000; ++i) { sl.lock(); ++shared; sl.unlock(); } });
    for (auto& t : ts) t.join();
    std::cout << "spinlock-protected counter " << shared << "\n";
}
