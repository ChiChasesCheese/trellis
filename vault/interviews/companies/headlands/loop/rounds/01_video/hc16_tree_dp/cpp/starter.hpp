// hc16 · Tree DP on a desk hierarchy — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Hint: build once with a BFS order (parents before children), then run every query over that order in reverse.
// parent[i] may be larger than i, so you cannot simply scan from n-1 down to 0.  No recursion (Part 4).
#pragma once

#include <climits>
#include <cstddef>
#include <stdexcept>
#include <utility>
#include <vector>

namespace desk {

/// |pnl| limit: keeps every sum <= 10^18, so nothing overflows long long.  Do not validate with std::llabs (UB on LLONG_MIN).
inline constexpr long long MAX_ABS_PNL = 1'000'000'000'000LL;
inline constexpr int MAX_DESKS = 1'000'000;

/// A selection: total = sum of the chosen desks' PnL; desks ascending.
struct Plan {
    long long total;
    std::vector<int> desks;
    friend bool operator==(const Plan&, const Plan&) = default;
};
/// Subtree summary: total PnL of the subtree rooted at `root`.
struct Subtree {
    int root;
    long long total;
    friend bool operator==(const Subtree&, const Subtree&) = default;
};

class DeskTree {
public:
    /// parent[i] = superior of desk i, -1 = root; n = 0 is a valid empty tree.
    /// Throws std::invalid_argument, checked in this order: "length mismatch", "too many desks", "invalid pnl",
    /// "invalid parent" (out of range or self), "invalid root" (n > 0 and not exactly one -1), "cycle" (root cannot reach every desk).
    /// The inputs are copied.
    static DeskTree of_parents(const std::vector<int>& /*parent*/, const std::vector<long long>& /*pnl*/) { throw std::logic_error("TODO"); }

    /// Part 2.  edges[i] = {a, b}: an undirected edge; orient the tree away from `root` (ignored when n = 0).
    /// Order: "length mismatch" (n < 0 or pnl.size() != n), "too many desks", "invalid pnl", "invalid root" (n > 0 and out of range),
    /// "invalid edge" (not two endpoints / out of range / self-loop), "not a tree" (edge count != max(0, n-1) or not every desk reachable).
    static DeskTree of_edges(int /*n*/, const std::vector<std::vector<int>>& /*edges*/, const std::vector<long long>& /*pnl*/, int /*root*/) { throw std::logic_error("TODO"); }

    int size() const { throw std::logic_error("TODO"); }
    /// Root desk; -1 for the empty tree.
    int root() const { throw std::logic_error("TODO"); }

    // ---------------- Part 1 ----------------

    /// Best total when no desk and its direct superior are both chosen.  Choosing nothing is allowed (empty / all-negative: 0).
    long long max_pnl() const { throw std::logic_error("TODO"); }

    // ---------------- Part 2 ----------------

    /// Same value plus the chosen desks.  Tie rule: v is chosen iff its superior is not chosen and "best total in v's subtree
    /// with v chosen" is strictly greater than "... with v not chosen"; equal means skip.  Desks ascending.
    Plan plan() const { throw std::logic_error("TODO"); }

    // ---------------- Part 3 (empty tree: std::out_of_range("empty tree")) ----------------

    /// Best non-empty downward path (each step goes to a child).
    long long max_down_path() const { throw std::logic_error("TODO"); }
    /// Best non-empty simple path anywhere (may go up then down, bending at one desk).
    long long max_path_sum() const { throw std::logic_error("TODO"); }
    /// Desk whose subtree total is largest; ties go to the smallest id.
    Subtree best_subtree() const { throw std::logic_error("TODO"); }

    // ---------------- Part 4 ----------------

    /// Textbook recursion; same answer as max_pnl().  Overflows the stack on a deep chain.  Every other method must survive a 10^5-deep chain.
    long long max_pnl_recursive() const { throw std::logic_error("TODO"); }
};

}  // namespace desk
