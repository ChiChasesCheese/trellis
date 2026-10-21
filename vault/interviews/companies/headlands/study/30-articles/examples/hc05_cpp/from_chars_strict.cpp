// Parsing integers: std::from_chars is the strict one, but you still have to check how much it consumed.
#include <charconv>
#include <cstdlib>
#include <iostream>
#include <string>
#include <string_view>

void show(std::string_view text) {
    long long v = 0;
    const auto [end, ec] = std::from_chars(text.data(), text.data() + text.size(), v);
    const bool whole = ec == std::errc{} && end == text.data() + text.size();
    std::cout << '"' << text << "\"  from_chars: " << (ec == std::errc::result_out_of_range ? "out of range" : ec == std::errc{} ? "ok" : "no digits")
              << ", consumed " << (end - text.data()) << "/" << text.size() << " -> " << (whole ? "ACCEPT" : "reject");
    std::string stoll_result;
    try {
        stoll_result = std::to_string(std::stoll(std::string(text)));
    } catch (const std::exception&) {
        stoll_result = "throws";
    }
    std::cout << "   |   stoll: " << stoll_result << "\n";
}

int main() {
    show("100");
    show("1.5");                    // from_chars stops at '.', so check the end pointer
    show("12abc");                  // stoll happily returns 12
    show("+5");                     // from_chars: no leading '+'; stoll accepts it
    show(" 7");                     // from_chars: no leading space; stoll skips it
    show("99999999999999999999");  // from_chars reports out of range
    show("-0");
}
