// A tiny lazy segment tree (range add, range max) with permanent tags, printed after every update.
// 4 elementary segments, leaves at nodes 4..7:           node 1  [0,3]
//                                                   node 2 [0,1]   node 3 [2,3]
//                                                 node 4 [0]  node 5 [1]  node 6 [2]  node 7 [3]
#include <algorithm>
#include <iostream>
#include <vector>

struct Tree {
    int size = 4;
    std::vector<int> mx = std::vector<int>(8, 0), add = std::vector<int>(8, 0);

    void range_add(int node, int nl, int nr, int l, int r, int delta) {
        if (l <= nl && nr <= r) { add[static_cast<std::size_t>(node)] += delta; mx[static_cast<std::size_t>(node)] += delta; return; }
        const int mid = nl + (nr - nl) / 2;
        if (l <= mid) range_add(2 * node, nl, mid, l, r, delta);
        if (r > mid) range_add(2 * node + 1, mid + 1, nr, l, r, delta);
        const auto n = static_cast<std::size_t>(node);
        mx[n] = add[n] + std::max(mx[2 * n], mx[2 * n + 1]);
    }
    int range_max(int node, int nl, int nr, int l, int r) const {
        const auto n = static_cast<std::size_t>(node);
        if (l <= nl && nr <= r) return mx[n];
        const int mid = nl + (nr - nl) / 2;
        int best = -1'000'000;
        if (l <= mid) best = std::max(best, range_max(2 * node, nl, mid, l, r));
        if (r > mid) best = std::max(best, range_max(2 * node + 1, mid + 1, nr, l, r));
        return best + add[n];
    }
    void print(const char* what) const {
        std::cout << what << "\n  mx : ";
        for (int i = 1; i < 8; ++i) std::cout << mx[static_cast<std::size_t>(i)] << " ";
        std::cout << "\n  add: ";
        for (int i = 1; i < 8; ++i) std::cout << add[static_cast<std::size_t>(i)] << " ";
        std::cout << "\n";
    }
};

int main() {
    Tree t;
    t.range_add(1, 0, 3, 0, 3, 1);  // covers the whole root: only add[1] and mx[1] change
    t.print("add [0,3]");
    t.range_add(1, 0, 3, 1, 2, 1);  // splits: node 5 (segment 1) and node 6 (segment 2) get tagged, parents recompute
    t.print("add [1,2]");
    std::cout << "max over [0,0] = " << t.range_max(1, 0, 3, 0, 0) << ", over [1,1] = " << t.range_max(1, 0, 3, 1, 1)
              << ", over [0,3] = " << t.range_max(1, 0, 3, 0, 3) << "\n";
    std::cout << "the tag on the root (" << t.add[1] << ") was never pushed down; the query adds it on the way back up\n";
}
