// Allocation count: node-based containers allocate per element; preallocated arrays do not allocate at all.
#include <cstdlib>
#include <iostream>
#include <list>
#include <map>
#include <new>
#include <vector>

static std::size_t g_news = 0;
void* operator new(std::size_t n) {
    ++g_news;
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

int main() {
    constexpr int orders = 1000;

    std::size_t before = g_news;
    std::map<long long, std::list<long long>> tree;
    for (int i = 0; i < orders; ++i) tree[1 + i % 50].push_back(i);  // 50 map nodes + 1000 list nodes
    std::cout << "map<price, list<order>>: " << g_news - before << " allocations for " << orders << " orders\n";

    struct Rec { long long id, qty; int prev, next; };
    std::vector<Rec> pool(orders);                                   // one allocation, made up front
    std::vector<int> head(51, -1), tail(51, -1);                     // one record per price level
    before = g_news;
    for (int i = 0; i < orders; ++i) {
        const int p = 1 + i % 50;
        pool[i] = {i, 1, tail[p], -1};
        if (tail[p] >= 0) pool[tail[p]].next = i; else head[p] = i;
        tail[p] = i;
    }
    std::cout << "preallocated arrays    : " << g_news - before << " allocations for " << orders << " orders\n";
}
