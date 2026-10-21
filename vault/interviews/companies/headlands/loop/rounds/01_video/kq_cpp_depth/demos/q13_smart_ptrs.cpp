// unique_ptr / shared_ptr / weak_ptr: ownership, cost, cycles.
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <new>

static int g_allocs = 0;
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n); if (!p) throw std::bad_alloc(); return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

struct Node {
    const char* name;
    std::shared_ptr<Node> next;          // strong link
    std::weak_ptr<Node> prev;            // weak link: does not keep the target alive
    explicit Node(const char* n) : name(n) {}
    ~Node() { std::printf("  ~Node(%s)\n", name); }
};
struct Leaky {                           // two strong links -> cycle
    const char* name;
    std::shared_ptr<Leaky> other;
    explicit Leaky(const char* n) : name(n) {}
    ~Leaky() { std::printf("  ~Leaky(%s)\n", name); }
};

int main() {
    std::printf("sizeof: raw=%zu unique_ptr=%zu shared_ptr=%zu\n", sizeof(int*), sizeof(std::unique_ptr<int>), sizeof(std::shared_ptr<int>));

    auto u = std::make_unique<int>(5);
    // auto u2 = u;                                         // does not compile: unique_ptr is move-only
    auto u2 = std::move(u);
    std::printf("after move: u=%s u2=%d\n", u ? "set" : "null", *u2);

    int base = g_allocs;
    std::shared_ptr<int> s1(new int(1));
    int two_step = g_allocs - base;
    base = g_allocs;
    auto s2 = std::make_shared<int>(1);
    std::printf("allocations: shared_ptr(new int) = %d, make_shared = %d\n", two_step, g_allocs - base);

    auto s3 = s2;
    std::printf("use_count = %ld\n", s2.use_count());
    std::weak_ptr<int> w = s2;
    s2.reset(); s3.reset();
    std::printf("after both reset: weak expired = %d, lock() %s\n", w.expired(), w.lock() ? "alive" : "null");

    std::printf("good list (weak back-link):\n");
    {
        auto a = std::make_shared<Node>("a");
        auto b = std::make_shared<Node>("b");
        a->next = b; b->prev = a;
    }
    std::printf("cycle of strong links (destructors never run):\n");
    {
        auto a = std::make_shared<Leaky>("a");
        auto b = std::make_shared<Leaky>("b");
        a->other = b; b->other = a;
        std::printf("  a.use_count = %ld\n", a.use_count());
    }
    std::printf("scope left; no ~Leaky line above means a leak\n");
}
