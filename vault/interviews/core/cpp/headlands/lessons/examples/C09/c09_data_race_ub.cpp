// EXPECT: run-fail
// SAN: thread
// C09: a data race (two threads, one write, no synchronisation) is UB. ThreadSanitizer finds it; ASan/UBSan do not.
#include <iostream>
#include <thread>

int counter = 0;                                  // plain int: not atomic, not locked

int main() {
    std::thread a([] { for (int i = 0; i < 100000; ++i) ++counter; });
    std::thread b([] { for (int i = 0; i < 100000; ++i) ++counter; });
    a.join(); b.join();
    std::cout << "counter = " << counter << " (expected 200000)\n";
}
