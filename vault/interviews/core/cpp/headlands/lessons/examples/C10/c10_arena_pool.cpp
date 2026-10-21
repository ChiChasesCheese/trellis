// SAN: none
// C10: custom allocation strategies: bump arena, fixed-size free-list pool, std::pmr. Why trading code avoids malloc on the hot path.
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <memory_resource>
#include <new>
#include <vector>

struct Order { std::uint64_t id; std::int64_t px; std::int64_t qty; std::uint64_t pad[5]; };    // 64 bytes

// [[snip:arena]]
// Bump allocator: allocation = move a pointer; free = nothing; reset() = free everything at once.
class Arena {
    unsigned char* base_;
    std::size_t cap_, used_ = 0;
public:
    explicit Arena(std::size_t cap) : base_(static_cast<unsigned char*>(std::malloc(cap))), cap_(cap) {}
    ~Arena() { std::free(base_); }
    Arena(const Arena&) = delete;
    Arena& operator=(const Arena&) = delete;
    void* allocate(std::size_t n, std::size_t align = alignof(std::max_align_t)) {
        std::size_t p = (used_ + align - 1) & ~(align - 1);            // round up to the alignment
        if (p + n > cap_) return nullptr;                              // a real arena would chain another block
        used_ = p + n;
        return base_ + p;
    }
    void reset() { used_ = 0; }
};
// [[/snip]]

// [[snip:pool]]
// Fixed-size pool: slots threaded into a free list stored INSIDE the free slots. O(1) alloc/free, no fragmentation.
template <class T, std::size_t N>
class Pool {
    union Slot { Slot* next; alignas(T) unsigned char bytes[sizeof(T)]; };
    Slot slots_[N];
    Slot* free_ = nullptr;
public:
    Pool() { for (std::size_t i = N; i-- > 0;) { slots_[i].next = free_; free_ = &slots_[i]; } }
    template <class... A> T* create(A&&... a) {
        if (!free_) return nullptr;                                    // pool exhausted: caller decides (no hidden malloc)
        Slot* s = free_; free_ = s->next;
        return new (s->bytes) T{std::forward<A>(a)...};
    }
    void destroy(T* p) {
        p->~T();
        Slot* s = reinterpret_cast<Slot*>(p);
        s->next = free_; free_ = s;
    }
};
// [[/snip]]

inline void escape(void* p) { asm volatile("" : : "r"(p) : "memory"); }   // tell the optimiser the pointer is used elsewhere

template <class F>
double ns_per_order(const char* name, long rounds, long batch, F&& f) {
    auto t0 = std::chrono::steady_clock::now();
    std::uint64_t sink = 0;
    for (long r = 0; r < rounds; ++r) sink += f(batch);
    auto t1 = std::chrono::steady_clock::now();
    double ns = std::chrono::duration<double, std::nano>(t1 - t0).count() / static_cast<double>(rounds * batch);
    std::cout << "  " << name << ": " << ns << " ns per create+destroy (sink " << (sink & 1) << ")\n";
    return ns;
}

int main() {
    const long B = 256;
    const long ROUNDS = std::getenv("QUICK") ? 2'000 : 200'000;
    std::cout << "create and destroy " << B << " Orders per round, " << ROUNDS << " rounds\n";

    ns_per_order("new / delete          ", ROUNDS, B, [](long n) {
        std::vector<Order*> v(n);
        for (long i = 0; i < n; ++i) v[i] = new Order{static_cast<std::uint64_t>(i), 100, 1, {}};
        std::uint64_t s = 0;
        for (long i = 0; i < n; ++i) { s += v[i]->id; delete v[i]; }
        return s;
    });
    static Pool<Order, 256> pool;
    ns_per_order("fixed pool (free list)", ROUNDS, B, [&](long n) {
        Order* v[256];
        for (long i = 0; i < n; ++i) v[i] = pool.create(Order{static_cast<std::uint64_t>(i), 100, 1, {}});
        std::uint64_t s = 0;
        for (long i = 0; i < n; ++i) { escape(v[i]); s += v[i]->id; pool.destroy(v[i]); }
        return s;
    });
    Arena arena(256 * sizeof(Order));
    ns_per_order("bump arena + reset    ", ROUNDS, B, [&](long n) {
        std::uint64_t s = 0;
        for (long i = 0; i < n; ++i) {
            Order* o = new (arena.allocate(sizeof(Order), alignof(Order))) Order{static_cast<std::uint64_t>(i), 100, 1, {}};
            escape(o);
            s += o->id;
        }
        arena.reset();                                                 // "free" all 256 at once
        return s;
    });
    ns_per_order("pmr monotonic + vector", ROUNDS, B, [](long n) {
        alignas(Order) unsigned char buf[256 * sizeof(Order) + 4096];
        std::pmr::monotonic_buffer_resource mr(buf, sizeof buf, std::pmr::null_memory_resource());
        std::pmr::vector<Order> v(&mr);
        v.reserve(n);
        for (long i = 0; i < n; ++i) v.push_back(Order{static_cast<std::uint64_t>(i), 100, 1, {}});
        std::uint64_t s = 0;
        escape(v.data());
        for (auto& o : v) s += o.id;
        return s;
    });
}
