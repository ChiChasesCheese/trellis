// C03: what does a shared_ptr copy cost? Raw pointer vs unique_ptr (by reference) vs shared_ptr (copy) vs shared_ptr (const&).
#include <atomic>
#include <chrono>
#include <iostream>
#include <memory>
#include <thread>
#include <vector>

struct Node { long v = 1; };

static long sink = 0;
template <class F>
double ns_per_op(const char* name, long n, F&& f) {
    auto t0 = std::chrono::steady_clock::now();
    f(n);
    auto t1 = std::chrono::steady_clock::now();
    double ns = std::chrono::duration<double, std::nano>(t1 - t0).count() / static_cast<double>(n);
    std::cout << "  " << name << ": " << ns << " ns/op\n";
    return ns;
}

// noinline so the optimiser cannot delete the copies we want to measure
[[gnu::noinline]] void take_raw(const Node* p) { sink += p->v; }
[[gnu::noinline]] void take_shared_copy(std::shared_ptr<Node> p) { sink += p->v; }
[[gnu::noinline]] void take_shared_ref(const std::shared_ptr<Node>& p) { sink += p->v; }

int main() {
    const long N = 20'000'000;
    auto sp = std::make_shared<Node>();
    Node* raw = sp.get();
    std::cout << "single thread:\n";
    ns_per_op("raw pointer          ", N, [&](long n) { for (long i = 0; i < n; ++i) take_raw(raw); });
    ns_per_op("shared_ptr const&    ", N, [&](long n) { for (long i = 0; i < n; ++i) take_shared_ref(sp); });
    ns_per_op("shared_ptr by value  ", N, [&](long n) { for (long i = 0; i < n; ++i) take_shared_copy(sp); });

    std::cout << "4 threads copying the SAME shared_ptr (one control block, contended atomic counter):\n";
    {
        auto t0 = std::chrono::steady_clock::now();
        std::vector<std::thread> ts;
        for (int t = 0; t < 4; ++t)
            ts.emplace_back([&] { long local = 0; for (long i = 0; i < N / 4; ++i) { auto c = sp; local += c->v; } sink += local; });
        for (auto& t : ts) t.join();
        auto t1 = std::chrono::steady_clock::now();
        std::cout << "  total wall " << std::chrono::duration<double, std::milli>(t1 - t0).count() << " ms for " << N
                  << " copies (" << std::chrono::duration<double, std::nano>(t1 - t0).count() / static_cast<double>(N / 4)
                  << " ns per copy per thread)\n";
    }
    std::cout << "(sink=" << sink << ")\n";
}
