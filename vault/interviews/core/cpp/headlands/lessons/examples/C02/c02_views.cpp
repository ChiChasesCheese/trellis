// C02: non-owning views (string_view, span) are cheap pointer+length pairs. Great parameters, dangerous members.
#include <iostream>
#include <numeric>
#include <span>
#include <string>
#include <string_view>
#include <vector>

// [[snip:sv]]
// Java: a String parameter is a cheap reference. C++: std::string by value copies; const std::string& forces
// a std::string to exist; std::string_view accepts literals, std::string, char arrays with no allocation.
int count_char(std::string_view s, char c) {
    int n = 0;
    for (char ch : s) n += (ch == c);
    return n;
}

std::string_view first_token(std::string_view s) {
    auto pos = s.find(' ');
    return s.substr(0, pos);                    // O(1): same bytes, new (pointer, length)
}
// [[/snip]]

// [[snip:span]]
long sum(std::span<const int> xs) {             // works for vector, array, C array, sub-ranges
    return std::accumulate(xs.begin(), xs.end(), 0L);
}
// [[/snip]]

int main() {
    std::string order = "BUY AAPL 100";
    std::cout << count_char("mississippi", 's') << " " << count_char(order, 'A') << "\n";
    std::string_view tok = first_token(order);
    std::cout << "first token: " << tok << " (" << tok.size() << " chars, no allocation)\n";

    std::vector<int> v{1, 2, 3, 4, 5, 6};
    int raw[3] = {10, 20, 30};
    std::cout << sum(v) << " " << sum(raw) << " " << sum(std::span<const int>(v).subspan(2, 3)) << "\n";

    std::cout << "sizeof(string_view)=" << sizeof(std::string_view) << " sizeof(span<int>)=" << sizeof(std::span<int>)
              << " (a pointer and a length)\n";
}
