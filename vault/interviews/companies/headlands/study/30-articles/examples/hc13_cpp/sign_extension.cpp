// Packing (generation, index) into a uint64_t: widen the index as UNSIGNED, or a high bit smears over the generation.
#include <cstdint>
#include <iostream>

int main() {
    const std::uint32_t generation = 5;
    const int index = -1;  // imagine a corrupted or sentinel index

    const std::uint64_t wrong = (static_cast<std::uint64_t>(generation) << 32) | static_cast<std::uint64_t>(index);  // int -> uint64_t sign-extends
    const std::uint64_t right = (static_cast<std::uint64_t>(generation) << 32) | static_cast<std::uint32_t>(index);

    std::cout << std::hex;
    std::cout << "sign-extended: 0x" << wrong << "  generation reads back as 0x" << static_cast<std::uint32_t>(wrong >> 32) << "\n";
    std::cout << "unsigned:      0x" << right << "  generation reads back as 0x" << static_cast<std::uint32_t>(right >> 32) << "\n";
}
