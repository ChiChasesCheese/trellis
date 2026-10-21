// C03: shared_ptr's control block, make_shared vs new, weak_ptr, and the reference cycle leak.
#include <cstdlib>
#include <iostream>
#include <memory>
#include <new>
#include <string>

// Count heap allocations by replacing global operator new.
static int g_allocs = 0;
void* operator new(std::size_t n) { ++g_allocs; if (void* p = std::malloc(n)) return p; throw std::bad_alloc(); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

struct Payload { long a[4]; };

// [[snip:allocs]]
void count_allocations() {
    int before = g_allocs;
    { std::shared_ptr<Payload> p(new Payload{}); }              // 1: the Payload, 2: the control block
    std::cout << "  shared_ptr(new T):  " << g_allocs - before << " allocations\n";
    before = g_allocs;
    { auto p = std::make_shared<Payload>(); }                   // object and control block in ONE block
    std::cout << "  make_shared<T>():   " << g_allocs - before << " allocation\n";
    before = g_allocs;
    { auto p = std::make_unique<Payload>(); }
    std::cout << "  make_unique<T>():   " << g_allocs - before << " allocation, no control block\n";
}
// [[/snip]]

// [[snip:counts]]
void use_counts() {
    auto sp = std::make_shared<std::string>("quote");
    std::weak_ptr<std::string> wp = sp;                         // observes; does not keep it alive
    std::cout << "  use_count=" << sp.use_count() << " weak expired=" << wp.expired() << "\n";
    {
        auto sp2 = sp;                                          // atomic increment of the strong count
        std::cout << "  use_count=" << sp.use_count() << "\n";
    }
    if (auto locked = wp.lock()) std::cout << "  lock() ok: " << *locked << "\n";   // upgrade, atomically
    sp.reset();
    std::cout << "  after reset: expired=" << wp.expired() << ", lock() null=" << (wp.lock() == nullptr) << "\n";
}
// [[/snip]]

// [[snip:cycle]]
static int g_alive = 0;
struct NodeBad {                       // parent <-> child both shared_ptr: a cycle nobody can free
    std::shared_ptr<NodeBad> other;
    NodeBad() { ++g_alive; }
    ~NodeBad() { --g_alive; }
};
struct NodeGood {                      // child holds a weak_ptr back to its parent
    std::shared_ptr<NodeGood> child;
    std::weak_ptr<NodeGood> parent;
    NodeGood() { ++g_alive; }
    ~NodeGood() { --g_alive; }
};

void cycles() {
    {
        auto a = std::make_shared<NodeBad>();
        auto b = std::make_shared<NodeBad>();
        a->other = b; b->other = a;
    }
    std::cout << "  cycle with shared_ptr both ways: alive after scope = " << g_alive << " (leaked)\n";
    int leaked = g_alive;
    {
        auto p = std::make_shared<NodeGood>();
        p->child = std::make_shared<NodeGood>();
        p->child->parent = p;          // weak back-pointer
    }
    std::cout << "  with weak_ptr back-pointer: newly leaked = " << g_alive - leaked << "\n";
}
// [[/snip]]

// [[snip:esft]]
struct Session : std::enable_shared_from_this<Session> {       // hand out shared_ptr to *this safely
    std::shared_ptr<Session> self() { return shared_from_this(); }
};
// [[/snip]]

int main() {
    std::cout << "sizeof(shared_ptr<Payload>)=" << sizeof(std::shared_ptr<Payload>) << " (object pointer + control-block pointer)\n";
    std::cout << "[allocations]\n"; count_allocations();
    std::cout << "[counts]\n"; use_counts();
    std::cout << "[cycles]\n"; cycles();
    auto s = std::make_shared<Session>();
    std::cout << "[enable_shared_from_this] use_count=" << s->self().use_count() - 1 << " before, same object: "
              << (s->self() == s) << "\n";
}
