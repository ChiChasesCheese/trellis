// Small unsigned types are promoted to (signed) int before arithmetic: `~x` and `x << n` do not stay 16 bits wide.
#include <cstdint>
#include <iostream>
#include <type_traits>

int main() {
    const std::uint16_t x = 0x00FF;
    static_assert(std::is_same_v<decltype(~x), int>);
    std::cout << std::hex << "~x as printed        = 0x" << ~x << "   (an int: 0xFFFFFF00)\n";
    std::cout << "~x == 0xFF00 ?         " << std::boolalpha << (~x == 0xFF00) << "\n";
    std::cout << "uint16_t(~x) == 0xFF00 ? " << (static_cast<std::uint16_t>(~x) == 0xFF00) << "\n";

    const std::uint32_t y = 0x000000FFu;
    static_assert(std::is_same_v<decltype(~y), std::uint32_t>);  // uint32_t is unsigned int: no promotion, so a 32-bit register is safe
    std::cout << "~y (uint32_t)         = 0x" << ~y << "\n";
}
