// std::from_chars: strict (no '+', no spaces, no 0x, no locale), but it succeeds on a valid PREFIX.
#include <charconv>
#include <cstdint>
#include <iostream>
#include <string_view>

void try_parse(std::string_view s, int base = 10) {
    std::uint64_t v = 0;
    const auto [end, ec] = std::from_chars(s.data(), s.data() + s.size(), v, base);
    const bool consumed_all = end == s.data() + s.size();
    std::cout << "'" << s << "' base " << base << ": ec=" << (ec == std::errc{} ? "ok" : ec == std::errc::result_out_of_range ? "out_of_range" : "invalid")
              << ", value=" << v << ", consumed all: " << std::boolalpha << consumed_all << "\n";
}

int main() {
    try_parse("12abc");        // ok, value 12, consumed all: false  <- the end pointer decides
    try_parse("+1");           // invalid: no plus sign
    try_parse("-1");           // invalid for an unsigned target
    try_parse("0xFF", 16);     // ok, value 0, stops at 'x': the prefix must be stripped by hand
    try_parse("FF", 16);       // ok
    try_parse("18446744073709551616");  // 2^64: out_of_range
}
