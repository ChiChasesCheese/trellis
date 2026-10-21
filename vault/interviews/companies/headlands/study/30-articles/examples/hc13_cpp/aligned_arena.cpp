// One aligned arena, records created in it with placement construction, freed with std::free through a unique_ptr.
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <new>

struct alignas(32) Slot {
    std::uint32_t gen;
    std::uint32_t next;
    long long id, px;
    int qty, side;
};
static_assert(sizeof(Slot) == 32 && alignof(Slot) == 32);

struct FreeDeleter { void operator()(void* p) const noexcept { std::free(p); } };

int main() {
    constexpr std::size_t count = 3;                       // 3 * 32 = 96 bytes: NOT a multiple of 64
    constexpr std::size_t bytes = count * sizeof(Slot);
    constexpr std::size_t rounded = (bytes + 63) / 64 * 64;  // aligned_alloc requires size % alignment == 0
    std::cout << "requested " << bytes << " bytes, allocating " << rounded << "\n";

    std::unique_ptr<void, FreeDeleter> arena(std::aligned_alloc(64, rounded));
    if (!arena) throw std::bad_alloc();
    auto* slots = static_cast<Slot*>(arena.get());
    std::uninitialized_value_construct_n(slots, count);   // the Slot objects now exist, all fields zero

    std::cout << "arena address % 64 = " << reinterpret_cast<std::uintptr_t>(slots) % 64 << "\n";
    for (std::size_t i = 0; i < count; ++i)
        std::cout << "slot " << i << " address % 64 = " << reinterpret_cast<std::uintptr_t>(&slots[i]) % 64 << ", id = " << slots[i].id << "\n";
    // Two slots share each 64-byte cache line (offsets 0 and 32): the pair is read with one cache miss.
}
