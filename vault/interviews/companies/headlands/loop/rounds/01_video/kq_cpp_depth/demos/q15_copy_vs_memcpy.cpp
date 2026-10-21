// std::copy vs memcpy vs memmove.
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <string>
#include <type_traits>
#include <vector>

struct SelfRef {                          // holds a pointer into its own storage
    char buf[8] = "abc";
    char* p = buf;
    SelfRef() = default;
    SelfRef(const SelfRef& o) { std::memcpy(buf, o.buf, sizeof buf); p = buf; }   // correct copy: re-point p
    SelfRef& operator=(const SelfRef& o) { std::memcpy(buf, o.buf, sizeof buf); p = buf; return *this; }
};
static_assert(!std::is_trivially_copyable_v<SelfRef>);
struct Pod { int a; double b; };
static_assert(std::is_trivially_copyable_v<int> && std::is_trivially_copyable_v<Pod>);
static_assert(!std::is_trivially_copyable_v<std::string>);

int copy_ints(const int* src, int* dst, std::size_t n) { std::copy(src, src + n, dst); return 0; }

int main() {
    int a[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    std::memmove(a + 2, a, 4 * sizeof(int));                  // overlapping ranges: memmove is defined
    std::printf("memmove overlap : %d %d %d %d %d %d %d %d\n", a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]);

    int b[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    std::copy_backward(b, b + 4, b + 6);                      // std::copy needs d_first outside [first,last); this form is OK
    std::printf("copy_backward   : %d %d %d %d %d %d %d %d\n", b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7]);

    SelfRef x;
    SelfRef raw_copy;
    std::memcpy(static_cast<void*>(&raw_copy), static_cast<void*>(&x), sizeof x);   // bitwise: copies p too
    SelfRef good = x;
    std::printf("memcpy copy's p points into the ORIGINAL: %s\n", raw_copy.p == x.buf ? "yes (bug)" : "no");
    std::printf("proper copy's p points into itself      : %s\n", good.p == good.buf ? "yes" : "no");

    std::vector<std::string> src{"alpha", std::string(40, 'b')}, dst(2);
    std::copy(src.begin(), src.end(), dst.begin());           // copy-assigns each element
    std::printf("std::copy on strings: %s %zu\n", dst[0].c_str(), dst[1].size());

    int s[4] = {9, 8, 7, 6}, t[4];
    copy_ints(s, t, 4);
    std::printf("copy_ints -> %d %d %d %d\n", t[0], t[1], t[2], t[3]);
}
