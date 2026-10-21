// C10: the allocator model. Containers take an Allocator template parameter; a counting allocator makes the calls visible.
#include <cstddef>
#include <iostream>
#include <list>
#include <memory>
#include <vector>

static int g_allocs = 0, g_frees = 0;
static std::size_t g_bytes = 0;

// [[snip:alloc]]
template <class T>
struct CountingAlloc {
    using value_type = T;
    CountingAlloc() = default;
    template <class U> CountingAlloc(const CountingAlloc<U>&) {}       // rebind: node containers allocate other types
    T* allocate(std::size_t n) {
        ++g_allocs; g_bytes += n * sizeof(T);
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t) noexcept { ++g_frees; ::operator delete(p); }
    template <class U> bool operator==(const CountingAlloc<U>&) const { return true; }
    template <class U> bool operator!=(const CountingAlloc<U>&) const { return false; }
};
// [[/snip]]

int main() {
    {
        std::vector<int, CountingAlloc<int>> v;
        for (int i = 0; i < 1000; ++i) v.push_back(i);
        std::cout << "vector of 1000 push_backs: " << g_allocs << " allocations, " << g_bytes << " bytes requested in total\n";
    }
    std::cout << "after destruction: allocs=" << g_allocs << " frees=" << g_frees << "\n";
    g_allocs = g_frees = 0; g_bytes = 0;
    {
        std::list<int, CountingAlloc<int>> l;
        for (int i = 0; i < 1000; ++i) l.push_back(i);
        std::cout << "list of 1000 push_backs  : " << g_allocs << " allocations (one per node), " << g_bytes << " bytes\n";
    }
    g_allocs = g_frees = 0;
    {
        std::vector<int, CountingAlloc<int>> v;
        v.reserve(1000);
        for (int i = 0; i < 1000; ++i) v.push_back(i);
        std::cout << "vector with reserve(1000): " << g_allocs << " allocation\n";
    }
}
