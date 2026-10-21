// Keeping malloc off the hot path: reserve, and a monotonic arena (std::pmr) built on a stack buffer.
#include <array>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <list>
#include <memory_resource>
#include <new>
#include <string>
#include <vector>

static long g_news = 0;
void* operator new(std::size_t n) { ++g_news; void* p = std::malloc(n); if (!p) throw std::bad_alloc(); return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

struct Order { long id; int qty; int px; };

template <class F> double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now(); f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    g_news = 0;
    { std::vector<Order> v; for (int i = 0; i < 1000; ++i) v.push_back({i, 1, 100}); }
    std::printf("vector push_back x1000, no reserve : %ld allocations\n", g_news);

    g_news = 0;
    { std::vector<Order> v; v.reserve(1000); for (int i = 0; i < 1000; ++i) v.push_back({i, 1, 100}); }
    std::printf("vector with reserve(1000)          : %ld allocation\n", g_news);

    g_news = 0;
    { std::list<Order> l; for (int i = 0; i < 1000; ++i) l.push_back({i, 1, 100}); }
    std::printf("std::list x1000                    : %ld allocations\n", g_news);

    g_news = 0;
    {
        alignas(std::max_align_t) std::array<std::byte, 64 * 1024> buf;            // storage on the stack
        std::pmr::monotonic_buffer_resource arena(buf.data(), buf.size(), std::pmr::null_memory_resource());
        std::pmr::list<Order> l(&arena);                                           // nodes come from `buf`
        for (int i = 0; i < 1000; ++i) l.push_back({i, 1, 100});
        std::pmr::vector<std::pmr::string> names(&arena);
        for (int i = 0; i < 100; ++i) names.emplace_back("a string long enough to leave the small-string buffer behind");
    }
    std::printf("pmr list + 100 pmr strings on arena: %ld allocations (all from the stack buffer)\n", g_news);

    // Heap churn vs arena reset
    double heap = ms([&] { for (int r = 0; r < 2000; ++r) { std::list<Order> l; for (int i = 0; i < 1000; ++i) l.push_back({i, 1, 100}); } });
    static std::array<std::byte, 64 * 1024> big;
    double arena_t = ms([&] {
        std::pmr::monotonic_buffer_resource arena(big.data(), big.size(), std::pmr::null_memory_resource());
        for (int r = 0; r < 2000; ++r) { arena.release(); std::pmr::list<Order> l(&arena); for (int i = 0; i < 1000; ++i) l.push_back({i, 1, 100}); }
    });
    std::printf("2000 x (build 1000-node list): malloc %.0f ms, arena %.0f ms\n", heap, arena_t);
}
