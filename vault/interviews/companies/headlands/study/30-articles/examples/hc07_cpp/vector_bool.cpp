// std::vector<bool> is a bit-packed container of proxies, not a vector of bool.
#include <cstdint>
#include <iostream>
#include <type_traits>
#include <vector>

int main() {
    std::vector<bool> bits(8);
    std::vector<std::uint8_t> bytes(8);
    static_assert(!std::is_same_v<decltype(bits[0]), bool&>);     // a proxy object, returned by value
    static_assert(std::is_same_v<decltype(bytes[0]), std::uint8_t&>);
    // auto& first = bits[0];     // does not compile: cannot bind a reference to a temporary proxy
    // bool* p = &bits[0];        // does not compile: no address
    std::cout << "sizeof(bits[0]) = " << sizeof(bits[0]) << " bytes (the proxy), sizeof(bytes[0]) = " << sizeof(bytes[0]) << "\n";
    bits[3] = true;               // works through the proxy
    std::cout << "bits[3] = " << bits[3] << "\n";
    // Neighbouring bits share a byte: two threads writing bits[0] and bits[1] race.  Use std::vector<std::uint8_t>.
}
