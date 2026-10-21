// C11: std::copy vs memcpy vs memmove. Overlap rules, trivially copyable, and the right way to shift elements.
#include <algorithm>
#include <cstring>
#include <iostream>
#include <string>
#include <type_traits>
#include <vector>

struct PodPoint { int x, y; };
struct HasString { std::string s; };
struct HasVirtual { virtual ~HasVirtual() = default; int v = 0; };
struct UserCopy { int v; UserCopy(const UserCopy& o) : v(o.v) {} };

// [[snip:traits]]
void traits() {
    std::cout << std::boolalpha;
    std::cout << "  int                trivially copyable: " << std::is_trivially_copyable_v<int> << "\n";
    std::cout << "  PodPoint           trivially copyable: " << std::is_trivially_copyable_v<PodPoint> << "\n";
    std::cout << "  std::string        trivially copyable: " << std::is_trivially_copyable_v<std::string> << "\n";
    std::cout << "  struct with string trivially copyable: " << std::is_trivially_copyable_v<HasString> << "\n";
    std::cout << "  class with virtual trivially copyable: " << std::is_trivially_copyable_v<HasVirtual> << "\n";
    std::cout << "  user-written copy  trivially copyable: " << std::is_trivially_copyable_v<UserCopy> << "\n";
}
// [[/snip]]

// [[snip:shift]]
void overlap() {
    std::vector<int> v{1, 2, 3, 4, 5, 6, 7, 8};
    // Shift elements [0,5) right by 2 -> destination range overlaps the source and starts INSIDE it.
    std::memmove(v.data() + 2, v.data(), 5 * sizeof(int));                   // memmove: defined for overlap
    std::cout << "  memmove right by 2     :";
    for (int x : v) std::cout << " " << x;
    std::cout << "\n";

    std::vector<int> w{1, 2, 3, 4, 5, 6, 7, 8};
    std::copy_backward(w.begin(), w.begin() + 5, w.begin() + 7);             // overlap + dest after source: copy_backward
    std::cout << "  copy_backward right by 2:";
    for (int x : w) std::cout << " " << x;
    std::cout << "\n";

    std::vector<int> u{1, 2, 3, 4, 5, 6, 7, 8};
    std::copy(u.begin() + 2, u.end(), u.begin());                            // dest BEFORE source: std::copy is fine
    std::cout << "  copy left by 2          :";
    for (int x : u) std::cout << " " << x;
    std::cout << "\n";
    // std::copy(u.begin(), u.begin()+5, u.begin()+2) would be UB: d_first must not lie in [first, last).
}
// [[/snip]]

// [[snip:strings]]
void non_trivial() {
    std::vector<std::string> src{"alpha-alpha-alpha-alpha-alpha-alpha", "beta-beta-beta-beta-beta-beta-beta"};
    std::vector<std::string> dst(2);
    std::copy(src.begin(), src.end(), dst.begin());                          // calls std::string::operator= per element: correct
    std::cout << "  std::copy of strings: " << dst[0].substr(0, 5) << " " << dst[1].substr(0, 4) << "; src untouched: " << src[0].size() << "\n";
    // std::memcpy(dst.data(), src.data(), 2 * sizeof(std::string));         // would copy raw pointers: two owners -> double free
}
// [[/snip]]

int main() {
    traits();
    overlap();
    non_trivial();
    PodPoint a[3] = {{1, 2}, {3, 4}, {5, 6}}, b[3];
    std::memcpy(b, a, sizeof a);                                              // fine: PodPoint is trivially copyable, no overlap
    static_assert(std::is_trivially_copyable_v<PodPoint>);
    std::cout << "  memcpy of PODs: b[2]=(" << b[2].x << "," << b[2].y << ")\n";
}
