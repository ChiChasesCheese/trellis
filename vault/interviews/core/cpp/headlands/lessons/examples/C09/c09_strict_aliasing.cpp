// SAN: none
// ASM: yes
// C09: strict aliasing. Accessing an object through a pointer of an unrelated type is UB; the optimiser relies on it.
#include <bit>
#include <cstdint>
#include <cstring>
#include <iostream>

// [[snip:alias]]
[[gnu::noinline]] int store_both(int* i, float* f) {
    *i = 1;
    *f = 2.0f;          // compiler: "an int* and a float* cannot alias" ...
    return *i;          // ... so *i is still 1: it never reloads
}
// [[/snip]]

// [[snip:safe]]
std::uint32_t bits_memcpy(float f) { std::uint32_t u; std::memcpy(&u, &f, sizeof u); return u; }   // legal; compiles to one mov
std::uint32_t bits_cast(float f) { return std::bit_cast<std::uint32_t>(f); }                       // C++20, constexpr-friendly
// std::uint32_t bits_bad(float f) { return *reinterpret_cast<std::uint32_t*>(&f); }                // UB: strict aliasing violation
// [[/snip]]

int main() {
    union { int i; float f; } storage{};
    int r = store_both(&storage.i, &storage.f);        // we lie to the compiler: both pointers name the same bytes
    std::cout << "store_both returned " << r << " (a literal reading of the code would give " << std::bit_cast<int>(2.0f) << ")\n";
    std::cout << "bits_memcpy(1.0f)=0x" << std::hex << bits_memcpy(1.0f) << " bits_cast(1.0f)=0x" << bits_cast(1.0f) << "\n";
}
