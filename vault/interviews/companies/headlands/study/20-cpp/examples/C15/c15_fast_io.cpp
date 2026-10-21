// RUN: $BIN < orders.txt
// C15: reading and parsing text input for coding rounds: fast iostream setup, getline, splitting, from_chars, formatted output.
#include <algorithm>
#include <charconv>
#include <cstdio>
#include <iomanip>
#include <iostream>
#include <map>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

// [[snip:split]]
std::vector<std::string_view> split(std::string_view s, char sep = ' ') {
    std::vector<std::string_view> out;
    while (!s.empty()) {
        auto pos = s.find(sep);
        if (pos == std::string_view::npos) { out.push_back(s); break; }
        if (pos > 0) out.push_back(s.substr(0, pos));       // skips empty fields from repeated separators
        s.remove_prefix(pos + 1);
    }
    return out;                                              // views into the caller's string: no copies
}
// [[/snip]]

// [[snip:parse]]
struct Order { bool buy; std::string sym; long qty; double px; };

template <class T>
std::optional<T> parse_num(std::string_view s) {            // no exceptions, no locale, no allocation
    T v{};
    auto [p, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    if (ec != std::errc{} || p != s.data() + s.size()) return std::nullopt;   // reject "12abc" and ""
    return v;
}

std::optional<Order> parse_order(std::string_view line) {
    auto f = split(line);
    if (f.size() != 4 || (f[0] != "BUY" && f[0] != "SELL")) return std::nullopt;
    auto q = parse_num<long>(f[2]);
    auto p = parse_num<double>(f[3]);
    if (!q || !p) return std::nullopt;
    return Order{f[0] == "BUY", std::string(f[1]), *q, *p};
}
// [[/snip]]

int main() {
    // [[snip:setup]]
    std::ios::sync_with_stdio(false);       // stop synchronising C++ streams with C stdio (do NOT mix printf/cin afterwards)
    std::cin.tie(nullptr);                  // don't flush cout before every cin read
    // [[/snip]]

    // [[snip:loop]]
    std::map<std::string, long> net;        // symbol -> net position
    std::map<std::string, double> notional;
    std::string line;
    int bad = 0;
    while (std::getline(std::cin, line)) {  // reads a whole line; strips the '\n'
        if (line.empty() || line[0] == '#') continue;
        if (auto o = parse_order(line)) {
            net[o->sym] += o->buy ? o->qty : -o->qty;
            notional[o->sym] += static_cast<double>(o->qty) * o->px;
        } else {
            ++bad;
            std::cerr << "skipped: " << line << "\n";
        }
    }
    // [[/snip]]

    // [[snip:out]]
    std::cout << std::fixed << std::setprecision(2);
    for (const auto& [sym, pos] : net)
        std::cout << std::left << std::setw(6) << sym << std::right << std::setw(6) << pos << std::setw(12) << notional[sym] << '\n';   // '\n', not std::endl
    std::cout << "bad lines: " << bad << '\n';
    // [[/snip]]
}
