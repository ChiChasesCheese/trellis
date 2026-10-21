// A fixed-size pool vs new / delete for objects that live a short while in a sliding window.
// The pool is a free list threaded through a vector of indices.  Build with -O2 and no sanitizers.
#include <chrono>
#include <cstdint>
#include <iostream>
#include <memory>
#include <vector>

struct Order { long long id, px; int qty, side; };

class IndexPool {
public:
    explicit IndexPool(std::uint32_t n) : next_(n), slots_(n) {
        for (std::uint32_t i = 0; i < n; ++i) next_[i] = i + 1 < n ? i + 1 : kEnd;
    }
    std::uint32_t allocate() { const auto i = head_; head_ = next_[i]; return i; }
    void free(std::uint32_t i) { next_[i] = head_; head_ = i; }
    Order& at(std::uint32_t i) { return slots_[i]; }
private:
    static constexpr std::uint32_t kEnd = 0xFFFFFFFFu;
    std::vector<std::uint32_t> next_;
    std::vector<Order> slots_;
    std::uint32_t head_ = 0;
};

int main() {
    constexpr int window = 100'000, messages = 20'000'000;
    long long sink = 0;
    {
        std::vector<std::unique_ptr<Order>> live(window);
        const auto t0 = std::chrono::steady_clock::now();
        for (int i = 0; i < messages; ++i) live[static_cast<std::size_t>(i % window)] = std::make_unique<Order>(Order{i, 18950 + (i & 63), 100 + (i & 7), i & 1});
        const auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        for (const auto& o : live) sink += o->qty;
        std::cout << "new / delete per message: " << ms << " ms\n";
    }
    {
        IndexPool pool(window);
        std::vector<std::uint32_t> live(window);
        for (auto& h : live) h = pool.allocate();
        const auto t0 = std::chrono::steady_clock::now();
        for (int i = 0; i < messages; ++i) {
            auto& h = live[static_cast<std::size_t>(i % window)];
            pool.free(h);
            h = pool.allocate();
            pool.at(h) = Order{i, 18950 + (i & 63), 100 + (i & 7), i & 1};
        }
        const auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        for (auto h : live) sink += pool.at(h).qty;
        std::cout << "pool free / allocate:     " << ms << " ms\n";
    }
    std::cout << "(checksum " << sink << ")\n";
}
