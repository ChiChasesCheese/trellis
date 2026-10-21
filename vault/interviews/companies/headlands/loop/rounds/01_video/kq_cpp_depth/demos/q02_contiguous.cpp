// A vector of structs is one block; a vector of pointers is a block of addresses.
#include <cstdio>
#include <cstdint>
#include <memory>
#include <vector>

struct Order { std::int64_t id; std::int32_t qty; std::int32_t px; };

int main() {
    std::vector<Order> flat(4);
    std::vector<std::unique_ptr<Order>> boxed;
    for (int i = 0; i < 4; ++i) boxed.push_back(std::make_unique<Order>());
    std::printf("sizeof(Order) = %zu\n", sizeof(Order));
    for (int i = 1; i < 4; ++i) {
        auto d_flat = reinterpret_cast<std::intptr_t>(&flat[i]) - reinterpret_cast<std::intptr_t>(&flat[i - 1]);
        std::printf("flat[%d]-flat[%d]   = %ld bytes\n", i, i - 1, static_cast<long>(d_flat));
    }
    // A pointer-based container: element addresses are whatever malloc returned.
    long gaps_ok = 0;
    for (int i = 1; i < 4; ++i) {
        auto d = reinterpret_cast<std::intptr_t>(boxed[i].get()) - reinterpret_cast<std::intptr_t>(boxed[i - 1].get());
        gaps_ok += (d == static_cast<long>(sizeof(Order)));
    }
    std::printf("boxed elements are adjacent only by luck of the allocator (adjacent pairs: %ld of 3)\n", gaps_ok);
    std::printf("sizeof(unique_ptr<Order>) = %zu: the vector stores addresses, not orders\n", sizeof(boxed[0]));
}
