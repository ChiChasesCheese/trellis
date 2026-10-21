// The bit-twiddling toolbox on an unsigned 32-bit register.
#include <bit>
#include <bitset>
#include <cstdint>
#include <cstdio>

constexpr std::uint32_t set_bit(std::uint32_t r, unsigned b)    { return r | (std::uint32_t{1} << b); }
constexpr std::uint32_t clear_bit(std::uint32_t r, unsigned b)  { return r & ~(std::uint32_t{1} << b); }
constexpr std::uint32_t toggle_bit(std::uint32_t r, unsigned b) { return r ^ (std::uint32_t{1} << b); }
constexpr bool test_bit(std::uint32_t r, unsigned b)            { return (r >> b) & 1u; }
constexpr std::uint32_t shl(std::uint32_t r, unsigned n)        { return n >= 32 ? 0 : r << n; }       // n >= 32 is UB for a raw <<
constexpr std::uint32_t rol(std::uint32_t r, unsigned n)        { n &= 31; return n ? (r << n) | (r >> (32 - n)) : r; }
constexpr bool is_pow2(std::uint32_t x)                          { return x && !(x & (x - 1)); }
constexpr std::uint32_t lowest_set(std::uint32_t x)              { return x & (~x + 1); }              // same as x & -x

constexpr int popcount_kernighan(std::uint32_t x)                { int c = 0; while (x) { x &= x - 1; ++c; } return c; }   // clears the lowest set bit each step
constexpr std::uint32_t field(std::uint32_t r, unsigned lo, unsigned width) { return (r >> lo) & ((std::uint32_t{1} << width) - 1); }

static void show(const char* what, std::uint32_t v) {
    std::printf("%-22s 0x%08X  %s  (%u)\n", what, v, std::bitset<32>(v).to_string().c_str(), v);
}

int main() {
    std::uint32_t r = 0xF0;
    show("start", r);
    show("set bit 0", set_bit(r, 0));
    show("clear bit 4", clear_bit(r, 4));
    show("toggle bit 31", toggle_bit(r, 31));
    show("shl 4", shl(r, 4));
    show("shl 32 (guarded)", shl(r, 32));
    show("rol 28", rol(0x12345678u, 28));
    show("std::rotl 28", std::rotl(0x12345678u, 28));
    show("not", ~r);
    std::printf("test_bit(r,5)=%d popcount=%d ctz=%d clz=%d is_pow2(64)=%d is_pow2(96)=%d lowest_set(0xF0)=0x%X\n",
                test_bit(r, 5), std::popcount(r), std::countr_zero(r), std::countl_zero(r), is_pow2(64), is_pow2(96), lowest_set(0xF0));

    std::printf("kernighan popcount(0xF0F0)=%d  field(0xABCD, lo=4, width=8)=0x%X\n", popcount_kernighan(0xF0F0u), field(0xABCDu, 4, 8));

    // Pitfalls
    std::uint8_t b = 0x0F;
    auto inv = ~b;                                              // promoted to int first!
    std::printf("~uint8_t(0x0F) has value %d, type size %zu (not 0xF0)\n", inv, sizeof(inv));
    std::printf("(uint8_t)~b = %d\n", static_cast<std::uint8_t>(~b));
    std::printf("printing a uint8_t with cout would print a char; with printf use %%u: %u\n", static_cast<unsigned>(b));
    int neg = -16;
    std::printf("-16 >> 2 = %d (arithmetic on this platform), as unsigned >> 2 = %u\n", neg >> 2, static_cast<unsigned>(neg) >> 2);
    std::printf("1u << 31 = %u (use unsigned literals for masks; 1 << 31 shifts into the sign bit of an int)\n", 1u << 31);
    std::printf("sizeof(1 << 3)=%zu sizeof(1LL << 40)=%zu\n", sizeof(1 << 3), sizeof(1LL << 40));
}
