// hc16 · Tree DP on a desk hierarchy — C++20 reference.  Statement: ../problem.md (Java: reference/DeskTree.java).
// Build once: validate, CSR child lists, a BFS order (parents before children).  Every query is a loop over that order
// in reverse (children before parents), so the stack depth is O(1).  Only max_pnl_recursive() recurses, on purpose.
#pragma once

#include <algorithm>
#include <climits>
#include <cstddef>
#include <stdexcept>
#include <utility>
#include <vector>

namespace desk {

/// |pnl| limit: every subtree sum / path sum / selection sum stays <= 10^6 * 10^12 = 10^18 < LLONG_MAX, so nothing overflows.
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
    /// parent[i] = superior of desk i, -1 = root; n = 0 is a valid empty tree.  Indices need not be smaller than i.
    /// Throws std::invalid_argument, checked in this order: "length mismatch", "too many desks", "invalid pnl",
    /// "invalid parent" (out of range or self), "invalid root" (n > 0 and not exactly one -1), "cycle".
    static DeskTree of_parents(const std::vector<int>& parent, const std::vector<long long>& pnl) {
        if (parent.size() != pnl.size()) throw std::invalid_argument("length mismatch");
        check_pnl(pnl);
        const int n = static_cast<int>(parent.size());
        int root = -1, roots = 0;
        for (int i = 0; i < n; ++i) {
            int p = parent[i];
            if (p == -1) {
                ++roots;
                root = i;
            } else if (p < 0 || p >= n || p == i) {
                throw std::invalid_argument("invalid parent");
            }
        }
        if (n > 0 && roots != 1) throw std::invalid_argument("invalid root");
        return DeskTree(parent, pnl, root);
    }

    /// edges[i] = {a, b}: an undirected edge; the tree is oriented away from `root` (ignored when n = 0).
    /// Order: "length mismatch" (n < 0 or pnl.size() != n), "too many desks", "invalid pnl", "invalid root" (n > 0),
    /// "invalid edge" (not two endpoints / out of range / self-loop), "not a tree" (edge count != max(0, n-1) or not
    /// every desk reachable from root).
    static DeskTree of_edges(int n, const std::vector<std::vector<int>>& edges, const std::vector<long long>& pnl, int root) {
        if (n < 0 || pnl.size() != static_cast<std::size_t>(n)) throw std::invalid_argument("length mismatch");
        check_pnl(pnl);
        if (n > 0 && (root < 0 || root >= n)) throw std::invalid_argument("invalid root");
        for (const auto& e : edges) {
            if (e.size() != 2 || e[0] < 0 || e[0] >= n || e[1] < 0 || e[1] >= n || e[0] == e[1]) throw std::invalid_argument("invalid edge");
        }
        if (edges.size() != static_cast<std::size_t>(std::max(0, n - 1))) throw std::invalid_argument("not a tree");
        if (n == 0) return DeskTree({}, {}, -1);
        std::vector<int> start(n + 1, 0);
        for (const auto& e : edges) {
            ++start[e[0] + 1];
            ++start[e[1] + 1];
        }
        for (int v = 0; v < n; ++v) start[v + 1] += start[v];
        std::vector<int> adj(2 * edges.size());
        std::vector<int> fill(start.begin(), start.end() - 1);
        for (const auto& e : edges) {
            adj[fill[e[0]]++] = e[1];
            adj[fill[e[1]]++] = e[0];
        }
        std::vector<int> parent(n, -2), queue;
        queue.reserve(n);
        parent[root] = -1;
        queue.push_back(root);
        for (std::size_t head = 0; head < queue.size(); ++head) {
            int v = queue[head];
            for (int i = start[v]; i < start[v + 1]; ++i) {
                int w = adj[i];
                if (parent[w] == -2) {
                    parent[w] = v;
                    queue.push_back(w);
                }
            }
        }
        if (queue.size() != static_cast<std::size_t>(n)) throw std::invalid_argument("not a tree");
        return DeskTree(std::move(parent), pnl, root);
    }

    int size() const { return n_; }
    /// Root desk; -1 for the empty tree.
    int root() const { return root_; }

    // ---------------- Part 1 ----------------

    /// Best total when no desk and its direct superior are both chosen.  Choosing nothing is allowed (empty / all-negative: 0).
    long long max_pnl() const {
        std::vector<long long> in, out;
        return solve_robber(in, out);
    }

    // ---------------- Part 2 ----------------

    /// Same value plus the chosen desks.  Tie rule: v is chosen iff its superior is not chosen and
    /// in[v] > out[v] (strictly better); equal means skip.  Desks ascending.
    Plan plan() const {
        std::vector<long long> in, out;
        long long total = solve_robber(in, out);
        std::vector<char> chosen(n_, 0);
        for (int v : order_) {
            int p = parent_[v];
            chosen[v] = (p < 0 || !chosen[p]) && in[v] > out[v];
        }
        Plan plan{total, {}};
        for (int v = 0; v < n_; ++v)
            if (chosen[v]) plan.desks.push_back(v);
        return plan;
    }

    // ---------------- Part 3 (empty tree: std::out_of_range("empty tree")) ----------------

    /// Best non-empty downward path (each step goes to a child).
    long long max_down_path() const {
        require_non_empty();
        return paths().first;
    }
    /// Best non-empty simple path anywhere (may go up then down, bending at one desk).
    long long max_path_sum() const {
        require_non_empty();
        return paths().second;
    }
    /// Desk whose subtree total is largest; ties go to the smallest id.
    Subtree best_subtree() const {
        require_non_empty();
        std::vector<long long> sum = pnl_;
        for (int i = n_ - 1; i > 0; --i) {
            int v = order_[i];
            sum[parent_[v]] += sum[v];
        }
        int best = 0;
        for (int v = 1; v < n_; ++v)
            if (sum[v] > sum[best]) best = v;
        return {best, sum[best]};
    }

    // ---------------- Part 4 ----------------

    /// Textbook recursion; same answer as max_pnl().  Overflows the stack on a deep chain — kept to show why.
    long long max_pnl_recursive() const {
        if (n_ == 0) return 0;
        auto [take, skip] = solve_recursive(root_);
        return std::max(take, skip);
    }

private:
    int n_;
    int root_;
    std::vector<long long> pnl_;
    std::vector<int> parent_;
    std::vector<int> order_;        // BFS order: a parent always precedes its children
    std::vector<int> child_start_;  // CSR: children of v are child_list_[child_start_[v] .. child_start_[v+1])
    std::vector<int> child_list_;

    DeskTree(std::vector<int> parent, std::vector<long long> pnl, int root)
        : n_(static_cast<int>(parent.size())), root_(root), pnl_(std::move(pnl)), parent_(std::move(parent)),
          child_start_(n_ + 1, 0), child_list_(std::max(0, n_ - 1)) {
        for (int v = 0; v < n_; ++v)
            if (parent_[v] >= 0) ++child_start_[parent_[v] + 1];
        for (int v = 0; v < n_; ++v) child_start_[v + 1] += child_start_[v];
        std::vector<int> fill(child_start_.begin(), child_start_.end() - 1);
        for (int v = 0; v < n_; ++v)
            if (parent_[v] >= 0) child_list_[fill[parent_[v]]++] = v;
        if (n_ > 0) {
            order_.reserve(n_);
            order_.push_back(root_);
            for (std::size_t head = 0; head < order_.size(); ++head) {
                int v = order_[head];
                for (int i = child_start_[v]; i < child_start_[v + 1]; ++i) order_.push_back(child_list_[i]);
            }
            if (order_.size() != static_cast<std::size_t>(n_)) throw std::invalid_argument("cycle");
        }
    }

    static void check_pnl(const std::vector<long long>& pnl) {
        if (pnl.size() > static_cast<std::size_t>(MAX_DESKS)) throw std::invalid_argument("too many desks");
        for (long long p : pnl)
            if (p > MAX_ABS_PNL || p < -MAX_ABS_PNL) throw std::invalid_argument("invalid pnl");  // no llabs: llabs(LLONG_MIN) is UB
    }

    void require_non_empty() const {
        if (n_ == 0) throw std::out_of_range("empty tree");
    }

    /// in[v] / out[v]: best total inside v's subtree with v chosen / not chosen.  Returns the root's max, 0 for the empty tree.
    long long solve_robber(std::vector<long long>& in, std::vector<long long>& out) const {
        in = pnl_;
        out.assign(n_, 0);
        for (int i = n_ - 1; i >= 0; --i) {
            int v = order_[i];
            int p = parent_[v];
            if (p >= 0) {
                in[p] += out[v];
                out[p] += std::max(in[v], out[v]);
            }
        }
        return n_ == 0 ? 0 : std::max(in[root_], out[root_]);
    }

    /// {best downward path, best path}; top1 / top2 = the two best child downward paths, negatives count as 0 (not taken).
    std::pair<long long, long long> paths() const {
        std::vector<long long> top1(n_, 0), top2(n_, 0);
        long long best_down = LLONG_MIN, best_path = LLONG_MIN;
        for (int i = n_ - 1; i >= 0; --i) {
            int v = order_[i];
            long long down = pnl_[v] + top1[v];
            best_down = std::max(best_down, down);
            best_path = std::max(best_path, pnl_[v] + top1[v] + top2[v]);
            int p = parent_[v];
            if (p >= 0 && down > 0) {
                if (down > top1[p]) {
                    top2[p] = top1[p];
                    top1[p] = down;
                } else if (down > top2[p]) {
                    top2[p] = down;
                }
            }
        }
        return {best_down, best_path};
    }

    std::pair<long long, long long> solve_recursive(int v) const {
        long long take = pnl_[v], skip = 0;
        for (int i = child_start_[v]; i < child_start_[v + 1]; ++i) {
            auto [ct, cs] = solve_recursive(child_list_[i]);
            take += cs;
            skip += std::max(ct, cs);
        }
        return {take, skip};
    }
};

}  // namespace desk
