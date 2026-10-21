// <bit> (C++20): rotate, popcount, leading / trailing zeros.  All defined for 0 and for any rotate count.
#include <bit>
#include <climits>
#include <cstdint>
#include <iostream>

int main() {
    const std::uint32_t x = 0x12345678u;
    std::cout << std::hex << "rotl(x, 4)  = 0x" << std::rotl(x, 4) << "\n";
    std::cout << "rotr(x, 4)  = 0x" << std::rotr(x, 4) << "\n";
    std::cout << "rotl(x, 36) = 0x" << std::rotl(x, 36) << "   (count taken mod 32)\n";
    std::cout << "rotl(x, INT_MAX) = 0x" << std::rotl(x, INT_MAX) << "\n" << std::dec;
    std::cout << "popcount(0xF0F0) = " << std::popcount(0xF0F0u) << "\n";
    std::cout << "countr_zero(0) = " << std::countr_zero(0u) << ", countl_zero(0) = " << std::countl_zero(0u)
              << "   (__builtin_ctz(0) and __builtin_clz(0) are undefined)\n";
    std::cout << "countl_zero(1) = " << std::countl_zero(1u) << ", countr_zero(0x80000000) = " << std::countr_zero(0x80000000u) << "\n";
}
