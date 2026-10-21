// Three traps when reading a fixed-width field from a byte buffer.
#include <bit>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <iostream>

int main() {
    // 1. plain `char` is signed here: a UTF-8 byte compares as a NEGATIVE number and slips through a range check
    const char e_acute = static_cast<char>(0xC3);
    std::cout << "(char)0xC3 < 'A'            : " << std::boolalpha << (e_acute < 'A') << "   (true: negative)\n";
    std::cout << "(unsigned char)0xC3 > 'Z'   : " << (static_cast<unsigned char>(e_acute) > 'Z') << "\n";

    // 2. `off + 8 > size` wraps around for a huge offset; `off > size - 8` (after size >= 8) does not
    const std::size_t size = 8, off = static_cast<std::size_t>(-1) - 3;
    std::cout << "off + 8 = " << (off + 8) << ", so `off + 8 > size` is " << (off + 8 > size) << "   (the huge offset passes!)\n";
    std::cout << "size >= 8 && off > size - 8 : " << (size >= 8 && off > size - 8) << "   (rejected)\n";

    // 3. load 8 bytes with memcpy (no aliasing / alignment problem), then fix the byte order: the first byte of the
    //    field must become the most significant byte
    const unsigned char field[8] = {'A', 'A', 'P', 'L', ' ', ' ', ' ', ' '};
    std::uint64_t word;
    std::memcpy(&word, field, 8);
    if constexpr (std::endian::native == std::endian::little) word = __builtin_bswap64(word);
    std::cout << "first byte after the swap   : " << static_cast<char>(word >> 56) << "\n";
}
