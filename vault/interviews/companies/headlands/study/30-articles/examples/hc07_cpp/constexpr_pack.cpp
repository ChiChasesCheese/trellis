// pack() and parse() are constexpr: a ticker literal is packed at compile time, and a bad literal is a compile error.
#include <iostream>

#include "../../../../loop/rounds/01_video/hc07_ticker_hash_map/cpp/reference.hpp"

using namespace tickers;

constexpr Key AAPL = codec::pack("AAPL");  // evaluated by the compiler
static_assert(AAPL == ((1ull << 35) | (1ull << 30) | (16ull << 25) | (12ull << 20)));
static_assert(codec::is_valid_key(AAPL));
static_assert(std::holds_alternative<codec::Invalid>(codec::parse("BRK.B")));  // invalid input is just a value
// constexpr Key bad = codec::pack("BRK.B");   // does not compile: the throw is reached during constant evaluation

int main() {
    LongTickerMap volume;
    volume.add(AAPL, 100);
    volume.add(AAPL, 50);
    std::cout << codec::unpack(AAPL) << " -> " << volume.get(AAPL, 0) << "\n";
}
