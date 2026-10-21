// Worker threads, exceptions and cooperative cancellation: an exception must not leave a thread body.
#include <atomic>
#include <chrono>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <stop_token>
#include <thread>
#include <vector>

int main() {
    constexpr int workers = 4;
    std::vector<std::exception_ptr> errors(workers);
    std::vector<long long> steps(workers, 0);
    std::stop_source stop;
    {
        std::vector<std::jthread> threads;
        for (int w = 0; w < workers; ++w)
            threads.emplace_back([&, w] {
                try {
                    for (long long i = 0; i < 50'000'000; ++i) {
                        if ((i & 0xFFF) == 0 && stop.stop_requested()) return;  // look at the flag every 4096 steps
                        if (w == 0 && i == 100'000) throw std::overflow_error("chunk 0 failed");
                        ++steps[static_cast<std::size_t>(w)];
                    }
                } catch (...) {
                    errors[static_cast<std::size_t>(w)] = std::current_exception();  // never let it escape the thread
                    stop.request_stop();
                }
            });
    }  // all jthreads joined here
    for (const auto& e : errors) {
        if (!e) continue;
        try { std::rethrow_exception(e); } catch (const std::exception& ex) { std::cout << "rethrown after join: " << ex.what() << "\n"; }
        break;
    }
    long long others = 0;
    for (int w = 1; w < workers; ++w) others += steps[static_cast<std::size_t>(w)];
    std::cout << "other workers stopped early: " << (others < 3LL * 50'000'000 ? "yes" : "no") << "\n";
}
