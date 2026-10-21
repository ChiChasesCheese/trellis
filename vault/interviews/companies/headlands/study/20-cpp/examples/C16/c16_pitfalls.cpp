// C16: the classic live-coding traps, each shown in its safe form (the trap is in the comment).
#include <climits>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>

int main() {
    // [[snip:unsigned]]
    std::vector<int> v{10, 20, 30};
    // for (size_t i = v.size() - 1; i >= 0; --i)   // TRAP: size_t is unsigned, i >= 0 is always true, wraps to 2^64-1
    for (std::size_t i = v.size(); i-- > 0;) std::cout << v[i] << " ";           // safe reverse loop with an unsigned index
    std::cout << "\n";
    std::vector<int> empty;
    // empty.size() - 1 is 18446744073709551615, not -1
    std::cout << "empty.size() - 1 = " << empty.size() - 1 << "; as int: " << static_cast<int>(empty.size()) - 1 << "\n";
    // [[/snip]]

    // [[snip:mid]]
    int lo = 2'000'000'000, hi = 2'100'000'000;
    // int mid = (lo + hi) / 2;                      // TRAP: lo + hi overflows int (UB)
    int mid = lo + (hi - lo) / 2;                    // safe midpoint
    std::cout << "mid = " << mid << "\n";
    // [[/snip]]

    // [[snip:div]]
    std::cout << "7/2 = " << 7 / 2 << ", 7.0/2 = " << 7.0 / 2 << ", -7/2 = " << -7 / 2 << ", -7%3 = " << -7 % 3
              << " (C++ truncates toward zero; % keeps the dividend's sign)\n";
    long cents = 1999;
    double dollars = cents / 100;                     // TRAP: integer division first -> 19
    double right = cents / 100.0;
    std::cout << "cents/100 = " << dollars << ", cents/100.0 = " << right << "\n";
    // [[/snip]]

    // [[snip:char]]
    char c = '7';
    int digit = c - '0';                              // char arithmetic: '7' is the number 55
    std::string s = "ab";
    std::cout << "digit " << digit << ", 'a'+1 = " << 'a' + 1 << " (an int!), static_cast<char>('a'+1) = " << static_cast<char>('a' + 1)
              << ", s + 'c' = " << s + 'c' << "\n";
    // [[/snip]]

    // [[snip:map]]
    std::map<std::string, int> m;
    if (m["x"] == 0) std::cout << "m[\"x\"] == 0, but size is now " << m.size() << " (operator[] inserted)\n";
    std::cout << "count() does not insert: " << m.count("y") << ", size " << m.size() << "\n";
    // [[/snip]]

    // [[snip:init]]
    std::vector<int> a(3, 7);                         // 3 elements of 7
    std::vector<int> b{3, 7};                         // 2 elements: 3 and 7 (braces prefer the initializer_list constructor)
    int uninit;                                       // TRAP: indeterminate value; reading it is UB
    int zero{};                                       // value-initialised to 0
    uninit = 5;
    std::cout << "vector(3,7).size()=" << a.size() << " vector{3,7}.size()=" << b.size() << " zero=" << zero << " uninit=" << uninit << "\n";
    // [[/snip]]
}
