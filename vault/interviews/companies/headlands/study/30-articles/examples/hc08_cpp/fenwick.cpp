// A Fenwick tree in 20 lines: point update, prefix sum, and "find the k-th" by binary descent.
#include <bit>
#include <iostream>
#include <vector>

struct Fenwick {
    int n;  // power of two
    std::vector<long long> t;
    explicit Fenwick(int size) : n(static_cast<int>(std::bit_ceil(static_cast<unsigned>(size)))), t(static_cast<std::size_t>(n) + 1, 0) {}
    void add(int i, long long d) { for (; i <= n; i += i & -i) t[static_cast<std::size_t>(i)] += d; }      // i & -i = lowest set bit
    long long prefix(int i) const { long long r = 0; for (; i > 0; i -= i & -i) r += t[static_cast<std::size_t>(i)]; return r; }
    int kth(long long k) const {  // smallest index whose prefix sum >= k (all values are 0 or 1 here)
        int pos = 0;
        for (int pw = n; pw > 0; pw >>= 1)
            if (pos + pw <= n && t[static_cast<std::size_t>(pos + pw)] < k) { pos += pw; k -= t[static_cast<std::size_t>(pos)]; }
        return pos + 1;
    }
};

int main() {
    Fenwick f(8);
    for (int i : {1, 2, 3, 5, 8}) f.add(i, 1);   // live slots
    f.add(2, -1);                                  // slot 2 removed: a hole
    std::cout << "live slots up to 5: " << f.prefix(5) << "\n";   // 1, 3, 5 -> 3
    std::cout << "3rd live slot: " << f.kth(3) << "\n";           // slot 5
    std::cout << "4th live slot: " << f.kth(4) << "\n";           // slot 8
    std::cout << "lowbit(12)=" << (12 & -12) << " lowbit(8)=" << (8 & -8) << "\n";
}
