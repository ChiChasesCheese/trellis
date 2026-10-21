// Shifting a 32-bit value by >= 32 is undefined in C++.  Two defined ways to get the hardware answer (0).
#include <cstdint>
#include <iostream>

std::uint32_t shl_branch(std::uint32_t x, int n) { return n >= 32 ? 0u : x << n; }

std::uint32_t shl_wide(std::uint32_t x, std::uint32_t n_clamped_to_32) {
    return static_cast<std::uint32_t>(static_cast<std::uint64_t>(x) << n_clamped_to_32);  // 64-bit shift by <= 32 is defined
}

int main() {
    const std::uint32_t x = 0xFFFFFFFFu;
    std::cout << "shl_branch(x, 32) = " << shl_branch(x, 32) << "\n";
    std::cout << "shl_wide(x, 32)   = " << shl_wide(x, 32) << "\n";
    std::cout << "shl_wide(x, 31)   = 0x" << std::hex << shl_wide(x, 31) << "\n";
    // `x << 32` itself is not run here: UBSan reports "shift exponent 32 is too large for 32-bit type"
}
