// SAN: none
// ASM: yes
// C11: what the compiler emits. All four copies of trivially copyable ints become a call to memmove/memcpy (or inline loads/stores).
#include <algorithm>
#include <cstddef>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

// [[snip:funcs]]
[[gnu::noinline]] void copy_std(const int* a, const int* b, int* out) { std::copy(a, b, out); }
[[gnu::noinline]] void copy_memcpy(const int* a, std::size_t n, int* out) { std::memcpy(out, a, n * sizeof(int)); }
[[gnu::noinline]] void copy_loop(const int* a, std::size_t n, int* __restrict out) { for (std::size_t i = 0; i < n; ++i) out[i] = a[i]; }
[[gnu::noinline]] void copy_fixed16(const int* a, int* out) { std::memcpy(out, a, 16 * sizeof(int)); }       // known size: inline
[[gnu::noinline]] void copy_strings(const std::string* a, const std::string* b, std::string* out) { std::copy(a, b, out); }
// [[/snip]]

int main() {
    std::vector<int> a{1, 2, 3, 4, 5}, b(5), c(5), d(5), e(16);
    copy_std(a.data(), a.data() + 5, b.data());
    copy_memcpy(a.data(), 5, c.data());
    copy_loop(a.data(), 5, d.data());
    std::vector<int> big(16, 7);
    copy_fixed16(big.data(), e.data());
    std::string s[2] = {"x", "y"}, t[2];
    copy_strings(s, s + 2, t);
    std::cout << b[4] << c[4] << d[4] << " " << e[15] << " " << t[1] << "\n";
}
