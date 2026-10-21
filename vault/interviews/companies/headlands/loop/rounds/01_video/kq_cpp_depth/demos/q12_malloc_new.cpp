// malloc gives raw bytes; new gives a constructed object. Also: placement new, bad_alloc, operator new override.
#include <cstdio>
#include <cstdlib>
#include <new>
#include <string>

struct Widget {
    std::string name = "default-name-longer-than-small-string-buffer";
    Widget() { std::printf("  Widget ctor\n"); }
    ~Widget() { std::printf("  Widget dtor\n"); }
};

static int g_news = 0;
static void escape(void* p) { asm volatile("" : : "r"(p) : "memory"); }   // keep the optimizer from deleting unused allocations
void* operator new(std::size_t n) { ++g_news; void* p = std::malloc(n); if (!p) throw std::bad_alloc(); return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

int main() {
    std::printf("new Widget:\n");
    Widget* a = new Widget;
    delete a;

    std::printf("placement new into malloc'd bytes:\n");
    void* raw = std::malloc(sizeof(Widget));                  // raw memory: no constructor ran
    Widget* b = new (raw) Widget;                             // construct in place
    b->~Widget();                                             // destroy by hand
    std::free(raw);

    std::printf("failure behaviour:\n");
    volatile std::size_t big = ~std::size_t{0} / 2;           // volatile: stop the optimizer assuming success
    void* huge = std::malloc(big);
    escape(huge);
    std::printf("  malloc(huge) -> %s\n", huge ? "non-null" : "NULL");
    try { escape(operator new(big)); } catch (const std::bad_alloc&) { std::printf("  new(huge)    -> throws std::bad_alloc\n"); }
    char* nothrow = new (std::nothrow) char[big];
    escape(nothrow);
    std::printf("  new(nothrow) -> %s\n", nothrow ? "non-null" : "NULL");

    int before = g_news;
    std::string s(100, 'x');                                  // heap buffer: operator new called
    std::printf("std::string(100,'x') called operator new %d time(s)\n", g_news - before);
}
