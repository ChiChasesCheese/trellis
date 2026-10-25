// hc16 · Tree DP on a desk hierarchy — C++20 tests.  Same cases as test/DeskTreeTest.java plus C++-only edge cases (tag "cpp"):
// std::llabs(LLONG_MIN) is UB (the binary runs under UBSan), copy / move of a built tree, stack overflow as a crash not an exception,
// narrowing of sizes.
#include <algorithm>
#include <atomic>
#include <climits>
#include <iostream>
#include <numeric>
#include <optional>
#include <random>
#include <string>
#include <utility>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace desk;

namespace desk {
std::ostream& operator<<(std::ostream& os, const Plan& p) {
    os << "Plan(" << p.total << ",[";
    for (std::size_t i = 0; i < p.desks.size(); ++i) os << (i ? "," : "") << p.desks[i];
    return os << "])";
}
std::ostream& operator<<(std::ostream& os, const Subtree& s) { return os << "Subtree(" << s.root << "," << s.total << ")"; }
}  // namespace desk

namespace {

using Ints = std::vector<int>;
using Longs = std::vector<long long>;
using Rows = std::vector<std::vector<int>>;
using Rng = std::mt19937_64;

//   0 (1)
//   ├── 1 (4) ── 3 (6), 4 (3)
//   └── 2 (-9) ── 5 (7), 6 (1)
const Ints SAMPLE_PARENT{-1, 0, 0, 1, 1, 2, 2};
const Longs SAMPLE_PNL{1, 4, -9, 6, 3, 7, 1};
constexpr long long BOUND = MAX_ABS_PNL;

DeskTree tree(const Ints& parent, const Longs& pnl) { return DeskTree::of_parents(parent, pnl); }
DeskTree sample() { return tree(SAMPLE_PARENT, SAMPLE_PNL); }
Plan plan_of(long long total, Ints desks) { return Plan{total, std::move(desks)}; }

/// Message of the std::invalid_argument thrown by f; a marker when something else (or nothing) happens.
template <class F> std::string iae(F f) {
    try {
        f();
    } catch (const std::invalid_argument& e) {
        return e.what();
    } catch (...) {
        return "<other exception>";
    }
    return "<no exception>";
}

constexpr std::size_t SMALL_STACK = 512 * 1024;
std::atomic<long long> sink{0};  // keeps the optimiser from discarding a result nobody reads

template <class F> auto on_stack(std::size_t bytes, F body) {
    using R = decltype(body());
    std::optional<R> result;
    mt::run_on_stack(bytes, [&] { result = body(); });
    return *result;
}

// ---------------------------------------------------------------- random trees and slow models

/// Random tree with shuffled labels; a small `reach` makes it deeper.  Returns parent[] with -1 at the root.
Ints random_parents(Rng& rng, int n, int reach) {
    Ints perm(n);
    std::iota(perm.begin(), perm.end(), 0);
    std::shuffle(perm.begin(), perm.end(), rng);
    Ints parent(n);
    parent[perm[0]] = -1;
    for (int i = 1; i < n; ++i) {
        int back = static_cast<int>(rng() % static_cast<unsigned>(std::min(i, reach)));
        parent[perm[i]] = perm[i - 1 - back];
    }
    return parent;
}
Longs random_pnl(Rng& rng, int n, int lo, int hi) {
    Longs pnl(n);
    for (auto& x : pnl) x = lo + static_cast<int>(rng() % static_cast<unsigned>(hi - lo + 1));
    return pnl;
}
int root_of(const Ints& parent) {
    for (std::size_t i = 0; i < parent.size(); ++i)
        if (parent[i] == -1) return static_cast<int>(i);
    return -1;
}
Ints children_of(const Ints& parent, int v) {
    Ints out;
    for (std::size_t i = 0; i < parent.size(); ++i)
        if (parent[i] == v) out.push_back(static_cast<int>(i));
    return out;
}
std::pair<long long, long long> model(const Ints& parent, const Longs& pnl, int v) {
    long long take = pnl[v], skip = 0;
    for (int c : children_of(parent, v)) {
        auto [ct, cs] = model(parent, pnl, c);
        take += cs;
        skip += std::max(ct, cs);
    }
    return {take, skip};
}
void model_plan(const Ints& parent, const Longs& pnl, int v, bool parent_chosen, std::vector<char>& chosen) {
    auto [take, skip] = model(parent, pnl, v);
    chosen[v] = !parent_chosen && take > skip;
    for (int c : children_of(parent, v)) model_plan(parent, pnl, c, chosen[v], chosen);
}
Ints model_desks(const Ints& parent, const Longs& pnl) {
    std::vector<char> chosen(parent.size(), 0);
    model_plan(parent, pnl, root_of(parent), false, chosen);
    Ints out;
    for (std::size_t i = 0; i < parent.size(); ++i)
        if (chosen[i]) out.push_back(static_cast<int>(i));
    return out;
}
long long brute_robber(const Ints& parent, const Longs& pnl) {
    int n = static_cast<int>(parent.size());
    long long best = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
        bool ok = true;
        long long sum = 0;
        for (int v = 0; v < n && ok; ++v) {
            if (!(mask >> v & 1)) continue;
            sum += pnl[v];
            if (parent[v] >= 0 && (mask >> parent[v] & 1)) ok = false;
        }
        if (ok) best = std::max(best, sum);
    }
    return best;
}
Ints chain_to_root(const Ints& parent, int v) {
    Ints out;
    for (int x = v; x >= 0; x = parent[x]) out.push_back(x);
    return out;
}
bool contains(const Ints& xs, int v) { return std::find(xs.begin(), xs.end(), v) != xs.end(); }
long long brute_path(const Ints& parent, const Longs& pnl) {
    int n = static_cast<int>(parent.size());
    long long best = LLONG_MIN;
    for (int u = 0; u < n; ++u) {
        Ints up = chain_to_root(parent, u);
        for (int v = u; v < n; ++v) {
            Ints vp = chain_to_root(parent, v);
            int lca = -1;
            for (int x : up)
                if (contains(vp, x)) { lca = x; break; }
            long long sum = 0;
            for (int x : up) { sum += pnl[x]; if (x == lca) break; }
            for (int x : vp) { if (x == lca) break; sum += pnl[x]; }
            best = std::max(best, sum);
        }
    }
    return best;
}
long long brute_down(const Ints& parent, const Longs& pnl) {
    long long best = LLONG_MIN;
    for (std::size_t d = 0; d < parent.size(); ++d) {
        long long sum = 0;
        for (int x : chain_to_root(parent, static_cast<int>(d))) {
            sum += pnl[x];
            best = std::max(best, sum);
        }
    }
    return best;
}
Subtree brute_subtree(const Ints& parent, const Longs& pnl) {
    Longs sum(parent.size(), 0);
    for (std::size_t d = 0; d < parent.size(); ++d)
        for (int x : chain_to_root(parent, static_cast<int>(d))) sum[x] += pnl[d];
    int best = 0;
    for (std::size_t v = 1; v < parent.size(); ++v)
        if (sum[v] > sum[best]) best = static_cast<int>(v);
    return {best, sum[best]};
}
Rows edges_of(const Ints& parent) {
    Rows out;
    for (std::size_t i = 0; i < parent.size(); ++i)
        if (parent[i] >= 0) out.push_back({static_cast<int>(i), parent[i]});
    return out;
}

constexpr int DEEP = 100'000;
Ints chain(int n, bool root_first) {
    Ints parent(n);
    for (int i = 0; i < n; ++i) parent[i] = root_first ? i - 1 : (i == n - 1 ? -1 : i + 1);
    return parent;
}
Longs ones(int n) { return Longs(n, 1); }
Ints stepped(int to_exclusive, int first, int step) {
    Ints out;
    for (int i = first; i < to_exclusive; i += step) out.push_back(i);
    return out;
}

}  // namespace

// ================================================ Part 1: build + best total

TEST(sample_tree, "part1") {
    auto t = sample();
    CHECK_EQ(t.size(), 7);
    CHECK_EQ(t.root(), 0);
    CHECK_EQ(t.max_pnl(), 18);
}

TEST(empty_tree_is_valid, "part1,edge") {
    auto t = tree({}, {});
    CHECK_EQ(t.size(), 0);
    CHECK_EQ(t.root(), -1);
    CHECK_EQ(t.max_pnl(), 0);
}

TEST(single_desk, "part1,edge") {
    CHECK_EQ(tree({-1}, {7}).max_pnl(), 7);
    CHECK_EQ(tree({-1}, {-7}).max_pnl(), 0);
    CHECK_EQ(tree({-1}, {0}).max_pnl(), 0);
}

TEST(all_negative_chooses_nothing, "part1,edge") { CHECK_EQ(tree({-1, 0, 1, 1}, {-1, -2, -3, -4}).max_pnl(), 0); }

TEST(parent_and_child_cannot_both_be_chosen, "part1") {
    CHECK_EQ(tree({-1, 0}, {3, 4}).max_pnl(), 4);
    CHECK_EQ(tree({-1, 0}, {3, -4}).max_pnl(), 3);
    CHECK_EQ(tree({-1, 0, 1}, {5, 1, 5}).max_pnl(), 10);
    CHECK_EQ(tree({-1, 0, 1}, {3, 5, 3}).max_pnl(), 6);
}

TEST(siblings_may_both_be_chosen, "part1") {
    CHECK_EQ(tree({-1, 0, 0, 0}, {10, 4, 4, 4}).max_pnl(), 12);
    CHECK_EQ(tree({-1, 0, 0, 0}, {13, 4, 4, 4}).max_pnl(), 13);
}

TEST(parent_index_may_be_larger_than_child_index, "part1,edge") {
    CHECK_EQ(tree({2, 2, -1}, {5, 6, 1}).max_pnl(), 11);
    CHECK_EQ(tree({1, 2, 3, -1}, {4, 1, 4, 1}).max_pnl(), 8);
}

TEST(root_is_not_always_the_first_desk, "part1,edge") {
    auto t = tree({1, -1, 1}, {1, 1, 1});
    CHECK_EQ(t.root(), 1);
    CHECK_EQ(t.max_pnl(), 2);
}

TEST(invalid_inputs, "part1,edge") {
    CHECK_EQ(iae([] { tree({-1, 0}, {1}); }), "length mismatch");
    CHECK_EQ(iae([] { tree({-1}, {BOUND + 1}); }), "invalid pnl");
    CHECK_EQ(iae([] { tree({-1}, {-BOUND - 1}); }), "invalid pnl");
    CHECK_EQ(iae([] { tree({-1, 5}, {1, 1}); }), "invalid parent");
    CHECK_EQ(iae([] { tree({-1, -2}, {1, 1}); }), "invalid parent");
    CHECK_EQ(iae([] { tree({-1, 1}, {1, 1}); }), "invalid parent");
    CHECK_EQ(iae([] { tree({1, 0}, {1, 1}); }), "invalid root");
    CHECK_EQ(iae([] { tree({-1, -1}, {1, 1}); }), "invalid root");
    CHECK_EQ(iae([] { tree({-1, 2, 1}, {1, 1, 1}); }), "cycle");
    CHECK_EQ(iae([] { tree({-1, 2, 3, 1, 0}, {1, 1, 1, 1, 1}); }), "cycle");
}

TEST(errors_are_checked_in_the_documented_order, "part1,edge") {
    CHECK_EQ(iae([] { tree({-1, 9}, {BOUND + 1}); }), "length mismatch");
    CHECK_EQ(iae([] { tree({-1, 9}, {1, BOUND + 1}); }), "invalid pnl");
    CHECK_EQ(iae([] { tree({-1, -1, 9}, {1, 1, 1}); }), "invalid parent");
    CHECK_EQ(iae([] { tree({-1, -1, 1}, {1, 1, 1}); }), "invalid root");
    CHECK_EQ(iae([] { tree(Ints(MAX_DESKS + 1), Longs(MAX_DESKS + 1)); }), "too many desks");
}

TEST(pnl_bounds_are_inclusive_and_llong_min_is_rejected, "part1,edge") {
    CHECK_EQ(tree({-1}, {BOUND}).max_pnl(), BOUND);
    CHECK_EQ(tree({-1}, {-BOUND}).max_pnl(), 0);
    CHECK_EQ(iae([] { tree({-1}, {LLONG_MIN}); }), "invalid pnl");
    CHECK_EQ(iae([] { tree({-1}, {LLONG_MAX}); }), "invalid pnl");
}

TEST(input_vectors_are_copied, "part1,edge") {
    Ints parent{-1, 0, 0};
    Longs pnl{1, 5, 5};
    auto t = tree(parent, pnl);
    pnl[1] = -100;
    parent[1] = 2;
    CHECK_EQ(t.max_pnl(), 10);
    CHECK_EQ(t.max_pnl(), 10);
}

TEST(no_overflow_at_the_limits, "part1,edge") {
    // star: root + 999'999 leaves, all at the PnL limit; choosing every leaf = 999'999 * 10^12
    int n = MAX_DESKS;
    Ints parent(n, 0);
    parent[0] = -1;
    auto t = tree(parent, Longs(n, BOUND));
    CHECK_EQ(t.max_pnl(), 999'999LL * BOUND);
    CHECK_EQ(t.best_subtree().total, static_cast<long long>(n) * BOUND);
    CHECK_EQ(t.max_path_sum(), 3 * BOUND);
    CHECK_EQ(t.max_down_path(), 2 * BOUND);
}

TEST(matches_brute_force_on_random_small_trees, "part1") {
    Rng rng(1);
    for (int round = 0; round < 400; ++round) {
        int n = 1 + static_cast<int>(rng() % 13);
        Ints parent = random_parents(rng, n, 1 + static_cast<int>(rng() % n));
        Longs pnl = random_pnl(rng, n, -6, 10);
        CHECK_EQ(tree(parent, pnl).max_pnl(), brute_robber(parent, pnl), "round " + std::to_string(round));
    }
}

// ================================================ Part 2: plan + edge list

TEST(sample_plan, "part2") {
    auto plan = sample().plan();
    CHECK_EQ(plan.total, 18);
    CHECK_EQ(plan.desks, (Ints{0, 3, 4, 5, 6}));
    CHECK_EQ(plan, plan_of(18, {0, 3, 4, 5, 6}));
}

TEST(empty_and_negative_plans, "part2,edge") {
    CHECK_EQ(tree({}, {}).plan(), plan_of(0, {}));
    CHECK_EQ(tree({-1, 0, 0}, {-1, -2, -3}).plan(), plan_of(0, {}));
    CHECK_EQ(tree({-1, 0, 0}, {0, 0, 0}).plan(), plan_of(0, {}));
}

TEST(ties_go_to_skipping_the_desk, "part2,edge") {
    CHECK_EQ(tree({-1, 0}, {5, 5}).plan(), plan_of(5, {1}));
    CHECK_EQ(tree({-1, 0, 0}, {6, 3, 3}).plan(), plan_of(6, {1, 2}));
    CHECK_EQ(tree({-1, 0, 1}, {3, 5, 3}).plan(), plan_of(6, {0, 2}));
    CHECK_EQ(tree({-1, 0, 1, 2}, {1, 5, 1, 5}).plan(), plan_of(10, {1, 3}));
}

TEST(zero_pnl_desk_is_never_chosen, "part2,edge") { CHECK_EQ(tree({-1, 0, 1}, {0, 4, 0}).plan(), plan_of(4, {1})); }

TEST(plan_is_valid_and_matches_the_tie_rule_on_random_trees, "part2") {
    Rng rng(2);
    for (int round = 0; round < 400; ++round) {
        int n = 1 + static_cast<int>(rng() % 30);
        Ints parent = random_parents(rng, n, 1 + static_cast<int>(rng() % n));
        Longs pnl = random_pnl(rng, n, -3, 6);
        auto t = tree(parent, pnl);
        auto plan = t.plan();
        CHECK_EQ(plan.total, t.max_pnl());
        CHECK_EQ(plan.desks, model_desks(parent, pnl), "round " + std::to_string(round));
        long long sum = 0;
        for (int v : plan.desks) {
            sum += pnl[v];
            CHECK(parent[v] < 0 || !contains(plan.desks, parent[v]), "adjacent desks chosen");
        }
        CHECK_EQ(plan.total, sum);
    }
}

TEST(edge_list_gives_the_same_tree, "part2") {
    Rows edges{{3, 1}, {0, 2}, {1, 0}, {4, 1}, {2, 5}, {6, 2}};
    auto t = DeskTree::of_edges(7, edges, SAMPLE_PNL, 0);
    CHECK_EQ(t.root(), 0);
    CHECK_EQ(t.max_pnl(), 18);
    CHECK_EQ(t.plan(), sample().plan());
    CHECK_EQ(t.best_subtree(), sample().best_subtree());
}

TEST(edge_list_with_another_root, "part2") {
    Rows edges{{0, 1}, {0, 2}, {1, 3}, {1, 4}, {2, 5}, {2, 6}};
    auto t = DeskTree::of_edges(7, edges, SAMPLE_PNL, 6);
    CHECK_EQ(t.root(), 6);
    CHECK_EQ(t.max_pnl(), 18);
    CHECK_EQ(t.max_path_sum(), 13);
}

TEST(edge_list_trivial_sizes, "part2,edge") {
    auto empty = DeskTree::of_edges(0, {}, {}, 0);
    CHECK_EQ(empty.size(), 0);
    CHECK_EQ(empty.root(), -1);
    CHECK_EQ(empty.plan(), plan_of(0, {}));
    CHECK_EQ(DeskTree::of_edges(0, {}, {}, 99).max_pnl(), 0);
    CHECK_EQ(DeskTree::of_edges(1, {}, {9}, 0).plan(), plan_of(9, {0}));
    CHECK_EQ(DeskTree::of_edges(2, {{1, 0}}, {5, 5}, 1).plan(), plan_of(5, {0}));
}

TEST(edge_list_errors, "part2,edge") {
    const Longs three{1, 2, 3};
    const Rows path{{0, 1}, {1, 2}};
    CHECK_EQ(iae([&] { DeskTree::of_edges(2, {{0, 1}}, three, 0); }), "length mismatch");
    CHECK_EQ(iae([&] { DeskTree::of_edges(-1, {}, {}, 0); }), "length mismatch");
    CHECK_EQ(iae([&] { DeskTree::of_edges(1, {}, {BOUND + 1}, 0); }), "invalid pnl");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, path, three, 3); }), "invalid root");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, path, three, -1); }), "invalid root");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, 1}, {1, 3}}, three, 0); }), "invalid edge");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, 1}, {1, 1}}, three, 0); }), "invalid edge");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, 1}, {1}}, three, 0); }), "invalid edge");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, 1}, {1, 2, 0}}, three, 0); }), "invalid edge");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, 1}, {}}, three, 0); }), "invalid edge");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, -1}, {1, 2}}, three, 0); }), "invalid edge");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, 1}}, three, 0); }), "not a tree");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, 1}, {1, 2}, {2, 0}}, three, 0); }), "not a tree");
    CHECK_EQ(iae([&] { DeskTree::of_edges(3, {{0, 1}, {1, 0}}, three, 0); }), "not a tree");
    CHECK_EQ(iae([&] { DeskTree::of_edges(4, {{0, 1}, {1, 0}, {2, 3}}, Longs(4), 0); }), "not a tree");
    CHECK_EQ(iae([&] { DeskTree::of_edges(0, {{0, 1}}, {}, 0); }), "invalid edge");
}

TEST(edge_list_matches_parents_on_random_trees, "part2") {
    Rng rng(3);
    for (int round = 0; round < 200; ++round) {
        int n = 1 + static_cast<int>(rng() % 40);
        Ints parent = random_parents(rng, n, 1 + static_cast<int>(rng() % n));
        Longs pnl = random_pnl(rng, n, -5, 9);
        Rows edges = edges_of(parent);
        std::shuffle(edges.begin(), edges.end(), rng);
        for (auto& e : edges)
            if (rng() & 1) std::swap(e[0], e[1]);
        auto via_parents = tree(parent, pnl);
        auto via_edges = DeskTree::of_edges(n, edges, pnl, via_parents.root());
        CHECK_EQ(via_parents.plan(), via_edges.plan());
        CHECK_EQ(via_parents.max_path_sum(), via_edges.max_path_sum());
        CHECK_EQ(via_parents.best_subtree(), via_edges.best_subtree());
        int other = static_cast<int>(rng() % n);
        auto rerooted = DeskTree::of_edges(n, edges, pnl, other);
        CHECK_EQ(rerooted.root(), other);
        CHECK_EQ(via_parents.max_pnl(), rerooted.max_pnl());
        CHECK_EQ(via_parents.max_path_sum(), rerooted.max_path_sum());
        CHECK_EQ(via_parents.plan().total, rerooted.plan().total);
    }
}

// ================================================ Part 3: paths and subtrees

TEST(sample_summaries, "part3") {
    auto t = sample();
    CHECK_EQ(t.max_down_path(), 11);
    CHECK_EQ(t.max_path_sum(), 13);
    CHECK_EQ(t.best_subtree(), (Subtree{0, 13}));
}

TEST(single_desk_paths, "part3,edge") {
    auto t = tree({-1}, {-4});
    CHECK_EQ(t.max_down_path(), -4);
    CHECK_EQ(t.max_path_sum(), -4);
    CHECK_EQ(t.best_subtree(), (Subtree{0, -4}));
}

TEST(all_negative_path_is_the_least_bad_single_desk, "part3,edge") {
    auto t = tree({-1, 0, 1}, {-5, -3, -8});
    CHECK_EQ(t.max_down_path(), -3);
    CHECK_EQ(t.max_path_sum(), -3);
    CHECK_EQ(t.best_subtree(), (Subtree{2, -8}));
}

TEST(bend_through_a_negative_desk_can_still_win, "part3,edge") {
    auto t = tree({-1, 0, 0}, {-1, 6, 7});
    CHECK_EQ(t.max_path_sum(), 12);
    CHECK_EQ(t.max_down_path(), 7);
    auto u = tree({-1, 0, 0}, {-10, 6, 7});
    CHECK_EQ(u.max_path_sum(), 7);
    CHECK_EQ(u.max_down_path(), 7);
}

TEST(bend_uses_the_two_best_branches_only, "part3,edge") {
    auto t = tree({-1, 0, 0, 0, 0}, {1, 5, 9, 7, -2});
    CHECK_EQ(t.max_path_sum(), 17);
    CHECK_EQ(t.max_down_path(), 10);
}

TEST(best_subtree_tie_goes_to_the_smallest_id, "part3,edge") {
    CHECK_EQ(tree({-1, 0, 0}, {-20, 5, 5}).best_subtree(), (Subtree{1, 5}));
    CHECK_EQ(tree({3, 3, 3, -1}, {2, 2, 2, -6}).best_subtree(), (Subtree{0, 2}));
    CHECK_EQ(tree({-1, 0}, {4, 0}).best_subtree(), (Subtree{0, 4}));
}

TEST(empty_tree_has_no_path, "part3,edge") {
    auto t = tree({}, {});
    CHECK_THROWS_AS(t.max_down_path(), std::out_of_range);
    CHECK_THROWS_AS(t.max_path_sum(), std::out_of_range);
    CHECK_THROWS_AS(t.best_subtree(), std::out_of_range);
    try {
        t.max_path_sum();
    } catch (const std::out_of_range& e) {
        CHECK_EQ(std::string(e.what()), "empty tree");
    }
}

TEST(paths_and_subtrees_match_brute_force_on_random_small_trees, "part3") {
    Rng rng(4);
    for (int round = 0; round < 400; ++round) {
        int n = 1 + static_cast<int>(rng() % 25);
        Ints parent = random_parents(rng, n, 1 + static_cast<int>(rng() % n));
        Longs pnl = random_pnl(rng, n, -9, 9);
        auto t = tree(parent, pnl);
        std::string ctx = "round " + std::to_string(round);
        CHECK_EQ(t.max_down_path(), brute_down(parent, pnl), ctx);
        CHECK_EQ(t.max_path_sum(), brute_path(parent, pnl), ctx);
        CHECK_EQ(t.best_subtree(), brute_subtree(parent, pnl), ctx);
    }
}

// ================================================ Part 4: depth and scale

TEST(deep_chain_does_not_need_a_deep_stack, "part4,edge") {
    // chain 0 -> 1 -> ... -> 99999, all 1: choose the odd ids (tie rule: an even-length chain skips its root)
    on_stack(SMALL_STACK, [] {
        auto t = tree(chain(DEEP, true), ones(DEEP));
        CHECK_EQ(t.max_pnl(), 50'000);
        auto plan = t.plan();
        CHECK_EQ(plan.total, 50'000);
        CHECK_EQ(plan.desks, stepped(DEEP, 1, 2));
        CHECK_EQ(t.max_down_path(), DEEP);
        CHECK_EQ(t.max_path_sum(), DEEP);
        CHECK_EQ(t.best_subtree(), (Subtree{0, DEEP}));
        return 0;
    });
}

TEST(deep_chain_with_the_root_last, "part4,edge") {
    // chain 99999 -> 99998 -> ... -> 0: the root has the largest id, so id order is the reverse of level order
    on_stack(SMALL_STACK, [] {
        auto t = tree(chain(DEEP, false), ones(DEEP));
        CHECK_EQ(t.root(), DEEP - 1);
        CHECK_EQ(t.max_pnl(), 50'000);
        CHECK_EQ(t.plan().desks, stepped(DEEP, 0, 2));
        CHECK_EQ(t.max_path_sum(), DEEP);
        CHECK_EQ(t.best_subtree(), (Subtree{DEEP - 1, DEEP}));
        return 0;
    });
}

TEST(deep_chain_from_an_edge_list, "part4,edge") {
    on_stack(SMALL_STACK, [] {
        Rows edges(DEEP - 1);
        for (int i = 0; i < DEEP - 1; ++i) edges[i] = {i + 1, i};
        auto t = DeskTree::of_edges(DEEP, edges, ones(DEEP), DEEP - 1);
        CHECK_EQ(t.max_pnl(), 50'000);
        CHECK_EQ(t.max_path_sum(), DEEP);
        CHECK_EQ(t.best_subtree(), (Subtree{DEEP - 1, DEEP}));
        return 0;
    });
}

TEST(deep_chain_with_alternating_signs, "part4,edge") {
    // +3 -1 +3 -1 ...: the +3 desks are never adjacent = 150000; whole chain = 100000; without the trailing -1 = 100001
    on_stack(SMALL_STACK, [] {
        Longs pnl(DEEP);
        for (int i = 0; i < DEEP; ++i) pnl[i] = i % 2 == 0 ? 3 : -1;
        auto t = tree(chain(DEEP, true), pnl);
        CHECK_EQ(t.max_pnl(), 150'000);
        CHECK_EQ(t.max_down_path(), 100'001);
        CHECK_EQ(t.max_path_sum(), 100'001);
        CHECK_EQ(t.best_subtree(), (Subtree{0, 100'000}));
        return 0;
    });
}

TEST(textbook_recursion_agrees_on_small_trees, "part4") {
    CHECK_EQ(sample().max_pnl_recursive(), 18);
    CHECK_EQ(tree({}, {}).max_pnl_recursive(), 0);
    Rng rng(5);
    for (int round = 0; round < 200; ++round) {
        int n = 1 + static_cast<int>(rng() % 60);
        auto t = tree(random_parents(rng, n, 1 + static_cast<int>(rng() % n)), random_pnl(rng, n, -8, 12));
        CHECK_EQ(t.max_pnl_recursive(), t.max_pnl());
    }
}

TEST(textbook_recursion_overflows_the_stack_on_a_deep_chain, "part4,edge") {
    // A stack overflow is SIGSEGV in C++, not an exception: it can only be observed from another process.
    bool survived = mt::child_survives([] {
        mt::run_on_stack(SMALL_STACK, [] {
            auto t = tree(chain(DEEP, true), ones(DEEP));
            sink = t.max_pnl_recursive();
        });
    });
    CHECK(!survived, "10^5 recursion levels cannot fit in 512 KiB: the child must die");
    // the iterative version survives on the same stack, and the recursive one is fine on a shallow chain
    CHECK_EQ(on_stack(SMALL_STACK, [] { return tree(chain(DEEP, true), ones(DEEP)).max_pnl(); }), 50'000);
    CHECK_EQ(on_stack(SMALL_STACK, [] { return tree(chain(100, true), ones(100)).max_pnl_recursive(); }), 50);
}

TEST(very_wide_tree, "part4,edge") {
    int n = DEEP;
    Ints parent(n, 0);
    parent[0] = -1;
    Longs pnl(n, 2);
    pnl[0] = 150'000;
    auto t = tree(parent, pnl);
    CHECK_EQ(t.max_pnl(), 2LL * (n - 1));
    CHECK_EQ(t.max_path_sum(), 150'004);
    CHECK_EQ(t.max_down_path(), 150'002);
    CHECK_EQ(t.best_subtree(), (Subtree{0, 150'000 + 2LL * (n - 1)}));
    Ints all(n - 1);
    std::iota(all.begin(), all.end(), 1);
    CHECK_EQ(t.plan(), plan_of(2LL * (n - 1), all));
}

TEST(million_desks_under_two_seconds, "part4,perf") {
    Rng rng(6);
    int n = 1'000'000;
    Ints parent = random_parents(rng, n, 4);  // small reach: a very deep random tree
    Longs pnl = random_pnl(rng, n, -1000, 1000);
    CHECK_WITHIN_MS(2000, {
        auto t = tree(parent, pnl);
        long long a = t.max_pnl();
        auto plan = t.plan();
        CHECK_EQ(a, plan.total);
        CHECK_GE(t.max_path_sum(), t.max_down_path());
        sink = t.best_subtree().total;
    });
}

TEST(million_desk_chain_on_a_small_stack, "part4,perf") {
    int n = 1'000'000;
    CHECK_WITHIN_MS(2000, {
        long long total = on_stack(SMALL_STACK, [&] {
            auto t = tree(chain(n, true), ones(n));
            CHECK_EQ(t.plan().total, 500'000);
            CHECK_EQ(t.max_path_sum(), n);
            return t.max_pnl();
        });
        CHECK_EQ(total, 500'000);
    });
}

// ================================================ C++-only

TEST(built_tree_can_be_copied_and_moved, "part1,cpp") {
    auto a = sample();
    DeskTree b = a;                 // copy: independent, same answers
    DeskTree c = std::move(a);      // move: the new owner answers the same
    CHECK_EQ(b.max_pnl(), 18);
    CHECK_EQ(c.max_pnl(), 18);
    CHECK_EQ(c.plan(), plan_of(18, {0, 3, 4, 5, 6}));
    b = tree({-1}, {1});            // assigning over a built tree
    CHECK_EQ(b.size(), 1);
    CHECK_EQ(c.size(), 7);
}

TEST(pnl_check_must_not_use_llabs, "part1,cpp") {
    // std::llabs(LLONG_MIN) overflows (UB; the binary runs under UBSan with -fno-sanitize-recover).  Compare against the bounds instead.
    CHECK_EQ(iae([] { tree({-1, 0}, {LLONG_MIN, 0}); }), "invalid pnl");
    CHECK_EQ(iae([] { tree({-1, 0}, {0, LLONG_MIN + 1}); }), "invalid pnl");
}

TEST(sizes_are_ints_not_size_t, "part1,cpp") {
    // size() / root() / Subtree::root are int: -1 for 'none' must stay representable (a size_t would wrap to 2^64-1)
    auto t = tree({}, {});
    CHECK_EQ(t.root(), -1);
    CHECK_LT(t.root(), 0);
    CHECK_EQ(t.size(), 0);
}

MT_MAIN()
