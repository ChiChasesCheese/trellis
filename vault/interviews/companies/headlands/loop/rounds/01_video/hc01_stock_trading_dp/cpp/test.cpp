// hc01 · Best time to buy and sell stock family — C++20 tests.  Same cases as test/StockTradingTest.java, plus C++-only
// edge cases (tag "cpp"): empty-span arithmetic, k + 1 overflow, sentinel overflow, 32-bit products, out-of-range enums,
// input left untouched, any contiguous container, optional plans.
#include <array>
#include <climits>
#include <iostream>
#include <random>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace stock;

namespace stock {
std::ostream& operator<<(std::ostream& os, const Trade& t) { return os << "Trade(" << t.buy_day << "," << t.sell_day << ")"; }
std::ostream& operator<<(std::ostream& os, const Plan& p) {
    os << "Plan{" << p.profit << ",[";
    for (const auto& t : p.trades) os << t << ";";
    return os << "]}";
}
std::ostream& operator<<(std::ostream& os, const Rules& r) {
    return os << "Rules{k=" << r.max_transactions << ",fee=" << r.fee << ",cd=" << r.cooldown << "}";
}
}  // namespace stock

namespace {

constexpr long long MAX = MAX_PRICE;
using V = std::vector<long long>;
using Ts = std::vector<Trade>;

template <class... T> V a(T... xs) { return V{static_cast<long long>(xs)...}; }

// Independent oracle: enumerate every (buy1 < sell1 < buy2 < sell2 ...) sequence; no state machine.
long long enumerate(const V& p, int from, int left, long long fee, int gap) {
    long long best = 0;
    if (left == 0) return 0;
    for (int b = from; b < static_cast<int>(p.size()); ++b)
        for (int s = b + 1; s < static_cast<int>(p.size()); ++s) {
            const long long net = p[static_cast<std::size_t>(s)] - p[static_cast<std::size_t>(b)] - fee;
            best = std::max(best, net + enumerate(p, s + 1 + gap, left - 1, fee, gap));
        }
    return best;
}
long long oracle(const V& p, int k, long long fee, bool cooldown) { return enumerate(p, 0, k, fee, cooldown ? 1 : 0); }

int below(std::mt19937_64& r, int bound) { return static_cast<int>(r() % static_cast<unsigned>(bound)); }

V random_prices(std::mt19937_64& r, int n, int bound) {
    V p(static_cast<std::size_t>(n));
    for (auto& x : p) x = below(r, bound);
    return p;
}

V walk(std::mt19937_64& r, int n) {
    V p(static_cast<std::size_t>(n));
    long long cur = 1'000'000;
    for (auto& x : p) {
        cur = std::max(1LL, std::min(MAX, cur + below(r, 2001) - 1000));
        x = cur;
    }
    return p;
}

}  // namespace

// ================================================ Part 1: one trade

TEST(lc121_samples, "part1") {
    CHECK_EQ(max_profit_once(a(7, 1, 5, 3, 6, 4)), 5);
    CHECK_EQ(max_profit_once(a(7, 6, 4, 3, 1)), 0);
    CHECK_EQ(max_profit_brute(a(7, 1, 5, 3, 6, 4)), 5);
    CHECK_EQ(max_profit_brute(a(7, 6, 4, 3, 1)), 0);
}

TEST(tiny_inputs, "part1,edge") {
    for (auto f : {&max_profit_brute, &max_profit_once}) {
        CHECK_EQ(f(a()), 0);
        CHECK_EQ(f(a(5)), 0);
        CHECK_EQ(f(a(3, 3, 3)), 0);
        CHECK_EQ(f(a(1, 2)), 1);
        CHECK_EQ(f(a(2, 1)), 0);
        CHECK_EQ(f(a(0, 0)), 0);
    }
}

TEST(lowest_price_comes_after_the_highest, "part1,edge") {
    // common mistake: global max - global min, ignoring "buy before sell"
    CHECK_EQ(max_profit_once(a(10, 9, 8, 1)), 0);
    CHECK_EQ(max_profit_once(a(5, 1, 5, 0, 4)), 4);
}

TEST(extreme_prices, "part1,edge") {
    CHECK_EQ(max_profit_once(a(0, MAX)), MAX);
    CHECK_EQ(max_profit_brute(a(0, MAX)), MAX);
    CHECK_EQ(max_profit_once(a(MAX, 0)), 0);
}

TEST(bad_inputs, "part1,edge") {
    // Java also tests null -> NullPointerException.  A std::span cannot be null: that whole class of bug does not exist.
    CHECK_THROWS_AS(max_profit_once(a(1, -1)), std::invalid_argument);
    CHECK_THROWS_AS(max_profit_once(a(1, MAX + 1)), std::invalid_argument);
    CHECK_THROWS_AS(max_profit_once(a(LLONG_MAX, 0)), std::invalid_argument);
    CHECK_THROWS_AS(max_profit_brute(a(-5)), std::invalid_argument);
    CHECK_THROWS_AS(max_profit_unlimited(a(0, 0, -1)), std::invalid_argument);
}

TEST(brute_and_linear_agree_on_random_inputs, "part1") {
    std::mt19937_64 r(0);
    for (int t = 0; t < 400; ++t) {
        const V p = random_prices(r, below(r, 30), 1 + below(r, 50));
        CHECK_EQ(max_profit_brute(p), max_profit_once(p));
    }
}

TEST(one_million_days_once, "part1,perf") {
    std::mt19937_64 r(0);
    const V p = walk(r, 1'000'000);
    CHECK_WITHIN_MS(2000, CHECK_GE(max_profit_once(p), 0););
}

// ================================================ Part 2: unlimited

TEST(lc122_samples, "part2") {
    CHECK_EQ(max_profit_unlimited(a(7, 1, 5, 3, 6, 4)), 7);
    CHECK_EQ(max_profit_unlimited(a(1, 2, 3, 4, 5)), 4);
    CHECK_EQ(max_profit_unlimited(a(7, 6, 4, 3, 1)), 0);
}

TEST(unlimited_edges, "part2,edge") {
    CHECK_EQ(max_profit_unlimited(a()), 0);
    CHECK_EQ(max_profit_unlimited(a(9)), 0);
    CHECK_EQ(max_profit_unlimited(a(4, 4, 4, 4)), 0);
}

TEST(huge_alternating_profit_does_not_overflow, "part2,edge") {
    // 0,MAX,0,MAX,... 2000 days: 1000 trades of 2^40 each = ~2^50
    V p(2000, 0);
    for (std::size_t i = 1; i < p.size(); i += 2) p[i] = MAX;
    CHECK_EQ(max_profit_unlimited(p), 1000 * MAX);
}

TEST(unlimited_matches_oracle, "part2") {
    std::mt19937_64 r(1);
    for (int t = 0; t < 300; ++t) {
        const V p = random_prices(r, below(r, 9), 1 + below(r, 20));
        CHECK_EQ(max_profit_unlimited(p), oracle(p, 99, 0, false));
    }
}

TEST(one_million_days_unlimited, "part2,perf") {
    std::mt19937_64 r(0);
    const V p = walk(r, 1'000'000);
    CHECK_WITHIN_MS(2000, CHECK_GE(max_profit_unlimited(p), 0););
}

// ================================================ Part 3: at most k

TEST(lc188_and_lc123_samples, "part3") {
    CHECK_EQ(max_profit_at_most(2, a(2, 4, 1)), 2);
    CHECK_EQ(max_profit_at_most(2, a(3, 2, 6, 5, 0, 3)), 7);
    CHECK_EQ(max_profit_at_most(2, a(3, 3, 5, 0, 0, 3, 1, 4)), 6);  // LC 123
    CHECK_EQ(max_profit_at_most(1, a(3, 3, 5, 0, 0, 3, 1, 4)), 4);
}

TEST(k_edges, "part3,edge") {
    CHECK_EQ(max_profit_at_most(0, a(1, 5, 2, 9)), 0);
    CHECK_EQ(max_profit_at_most(3, a()), 0);
    CHECK_EQ(max_profit_at_most(3, a(4)), 0);
    CHECK_EQ(max_profit_at_most(1, a(7, 1, 5, 3, 6, 4)), max_profit_once(a(7, 1, 5, 3, 6, 4)));
    CHECK_THROWS_AS(max_profit_at_most(-1, a(1, 2)), std::invalid_argument);
}

TEST(huge_k_must_not_allocate_k_sized_tables, "part3,edge") {
    const V p = a(7, 1, 5, 3, 6, 4);
    CHECK_EQ(max_profit_at_most(INT_MAX, p), 7);  // new vector(k + 1) would be signed overflow, then a 51 GB allocation
    CHECK_EQ(max_profit_at_most(1'000'000'000, p), 7);
    CHECK_EQ(max_profit_at_most(3, p), 7);  // k == n / 2 boundary
}

TEST(matches_oracle_and_is_monotone_in_k, "part3") {
    std::mt19937_64 r(2);
    for (int t = 0; t < 300; ++t) {
        const V p = random_prices(r, below(r, 10), 1 + below(r, 25));
        long long prev = 0;
        for (int k = 0; k <= 5; ++k) {
            const long long got = max_profit_at_most(k, p);
            CHECK_EQ(got, oracle(p, k, 0, false), "k=" + std::to_string(k));
            CHECK_GE(got, prev, "profit must not decrease when k grows");
            prev = got;
        }
    }
}

TEST(two_hundred_thousand_days_fifty_transactions, "part3,perf") {
    std::mt19937_64 r(0);
    const V p = walk(r, 200'000);
    CHECK_WITHIN_MS(2000, CHECK_GE(max_profit_at_most(50, p), 0););
}

TEST(one_million_days_two_transactions, "part3,perf") {
    std::mt19937_64 r(0);
    const V p = walk(r, 1'000'000);
    CHECK_WITHIN_MS(2000, CHECK_GE(max_profit_at_most(2, p), 0););
}

// ================================================ Part 4: cooldown / fee / plan

TEST(lc309_and_lc714_samples, "part4") {
    const auto cd = Rules::unlimited().with_cooldown(true);
    CHECK_EQ(max_profit(cd, a(1, 2, 3, 0, 2)), 3);
    CHECK_EQ(max_profit(cd, a(1)), 0);
    CHECK_EQ(max_profit(Rules::unlimited().with_fee(2), a(1, 3, 2, 8, 4, 9)), 8);
    CHECK_EQ(max_profit(Rules::unlimited().with_fee(3), a(1, 3, 7, 5, 10, 3)), 6);
}

TEST(rules_reduce_to_earlier_parts, "part4") {
    std::mt19937_64 r(3);
    for (int t = 0; t < 100; ++t) {
        const V p = walk(r, 50 + below(r, 50));
        CHECK_EQ(max_profit(Rules::at_most(1), p), max_profit_once(p));
        CHECK_EQ(max_profit(Rules::unlimited(), p), max_profit_unlimited(p));
        CHECK_EQ(max_profit(Rules::at_most(4), p), max_profit_at_most(4, p));
    }
}

TEST(fee_and_cooldown_edges, "part4,edge") {
    CHECK_EQ(max_profit(Rules::unlimited().with_fee(100), a(1, 5, 2, 9)), 0);  // fee above every spread
    CHECK_EQ(max_profit(Rules::unlimited().with_fee(4), a(1, 5)), 0);          // fee == spread: net 0 = no trade
    CHECK_EQ(max_profit(Rules::unlimited().with_fee(3), a(1, 5)), 1);
    CHECK_EQ(max_profit(Rules::unlimited().with_cooldown(true), a(1, 2, 1, 2)), 1);  // cannot sell day 1 and buy day 2
    CHECK_EQ(max_profit(Rules::unlimited(), a(1, 2, 1, 2)), 2);
    CHECK_EQ(max_profit(Rules::at_most(0), a(1, 9)), 0);
}

TEST(rules_are_validated, "part4,edge") {
    CHECK_THROWS_AS(Rules::at_most(-1), std::invalid_argument);
    CHECK_THROWS_AS(Rules::unlimited().with_fee(-1), std::invalid_argument);
    CHECK_THROWS_AS(Rules::unlimited().with_fee(MAX + 1), std::invalid_argument);
    CHECK_NOTHROW(Rules::unlimited().with_fee(MAX));
}

TEST(every_rule_combination_matches_oracle, "part4") {
    std::mt19937_64 r(4);
    for (int t = 0; t < 400; ++t) {
        const V p = random_prices(r, below(r, 10), 1 + below(r, 25));
        const int k = below(r, 5);
        const long long fee = below(r, 4);
        const bool cd = below(r, 2) == 1;
        const Rules rules(k, fee, cd);
        CHECK_EQ(max_profit(rules, p), oracle(p, k, fee, cd), "rules");
        CHECK_EQ(plan(rules, p).profit, oracle(p, k, fee, cd), "plan");
    }
}

TEST(plan_gives_the_obvious_trades, "part4") {
    const auto up = plan(Rules::unlimited(), a(7, 1, 5, 3, 6, 4));
    CHECK_EQ(up.profit, 7);
    const Ts up_expected{Trade(1, 2), Trade(3, 4)};
    CHECK_EQ(up.trades, up_expected);
    const auto cd = plan(Rules::unlimited().with_cooldown(true), a(1, 2, 3, 0, 2));
    CHECK_EQ(cd.profit, 3);
    const Ts cd_expected{Trade(0, 1), Trade(3, 4)};
    CHECK_EQ(cd.trades, cd_expected);
    const auto one = plan(Rules::at_most(1), a(7, 1, 5, 3, 6, 4));
    const Ts one_expected{Trade(1, 4)};
    CHECK_EQ(one.trades, one_expected);
    CHECK_EQ(one.profit, 5);
}

TEST(plan_of_nothing, "part4,edge") {
    const Plan nothing{0, {}};
    CHECK_EQ(plan(Rules::unlimited(), a()), nothing);
    CHECK_EQ(plan(Rules::unlimited(), a(4)), nothing);
    CHECK_EQ(plan(Rules::unlimited(), a(5, 4, 3)), nothing);
    CHECK_EQ(plan(Rules::at_most(0), a(1, 9)), nothing);
    CHECK_EQ(plan(Rules::unlimited().with_fee(50), a(1, 9, 1, 9)), nothing);
}

namespace {
/// Independent check: time-ordered, non-overlapping, cooldown, count, each net > 0, sum == profit.
void assert_valid_plan(const Rules& rules, const V& p, const Plan& pl) {
    long long sum = 0;
    int prev_sell = -10;
    CHECK_LE(pl.trades.size(), static_cast<std::size_t>(rules.max_transactions));
    for (const Trade& t : pl.trades) {
        if (prev_sell >= 0) CHECK_GT(t.buy_day, prev_sell, "trades overlap");
        if (rules.cooldown && prev_sell >= 0) CHECK_GE(t.buy_day, prev_sell + 2, "cooldown violated");
        CHECK_LT(t.sell_day, static_cast<int>(p.size()));
        const long long net = p[static_cast<std::size_t>(t.sell_day)] - p[static_cast<std::size_t>(t.buy_day)] - rules.fee;
        CHECK_GT(net, 0, "non-positive trade");
        sum += net;
        prev_sell = t.sell_day;
    }
    CHECK_EQ(pl.profit, sum);
}
}  // namespace

TEST(plan_is_always_a_valid_plan, "part4") {
    std::mt19937_64 r(5);
    for (int t = 0; t < 400; ++t) {
        const V p = random_prices(r, below(r, 40), 1 + below(r, 30));
        const Rules rules(below(r, 2) == 1 ? Rules::UNLIMITED : below(r, 6), below(r, 4), below(r, 2) == 1);
        const Plan pl = plan(rules, p);
        CHECK_EQ(pl.profit, max_profit(rules, p));
        assert_valid_plan(rules, p, pl);
        CHECK_EQ(replay(rules, p, pl.trades), pl.profit);
    }
}

TEST(plan_refuses_huge_tables, "part4,edge") {
    const V p(100'000, 0);
    CHECK_THROWS_AS(plan(Rules::at_most(50'000 - 1), p), std::invalid_argument);
}

TEST(state_machine_transitions, "part4") {
    const auto cd = Rules::unlimited().with_cooldown(true);
    const auto plain = Rules::unlimited();
    CHECK_EQ(after_buy(State::FREE), State::HOLD);
    CHECK_EQ(after_sell(State::HOLD, cd), State::COOL);
    CHECK_EQ(after_sell(State::HOLD, plain), State::FREE);
    CHECK_EQ(after_rest(State::COOL), State::FREE);
    CHECK_EQ(after_rest(State::FREE), State::FREE);
    CHECK_EQ(after_rest(State::HOLD), State::HOLD);
    CHECK_THROWS_AS(after_buy(State::COOL), IllegalState);
    CHECK_THROWS_AS(after_buy(State::HOLD), IllegalState);
    CHECK_THROWS_AS(after_sell(State::FREE, plain), IllegalState);
    CHECK_THROWS_AS(after_sell(State::COOL, cd), IllegalState);
}

TEST(replay_accepts_legal_and_computes_profit, "part4") {
    const V p = a(1, 2, 3, 0, 2);
    const Ts two{Trade(0, 1), Trade(3, 4)};
    CHECK_EQ(replay(Rules::unlimited().with_cooldown(true), p, two), 3);
    CHECK_EQ(replay(Rules::unlimited().with_fee(1), p, two), 3 - 2);  // fee on every sell
    CHECK_EQ(replay(Rules::unlimited(), p, {}), 0);
}

TEST(replay_rejects_illegal_plans, "part4,edge") {
    const V p = a(1, 2, 3, 0, 2, 5);
    const auto cd = Rules::unlimited().with_cooldown(true);
    const auto plain = Rules::unlimited();
    const Ts overlap{Trade(0, 3), Trade(1, 4)};
    CHECK_THROWS_AS(replay(plain, p, overlap), std::invalid_argument);
    const Ts buy_in_cooldown{Trade(0, 1), Trade(2, 5)};  // sell day 1, buy day 2
    CHECK_THROWS_AS(replay(cd, p, buy_in_cooldown), std::invalid_argument);
    CHECK_EQ(replay(plain, p, buy_in_cooldown), 3);  // the same plan is legal without cooldown: (2-1) + (5-3)
    const Ts two{Trade(0, 1), Trade(3, 4)};
    CHECK_THROWS_AS(replay(Rules::at_most(1), p, two), std::invalid_argument);  // more than k trades
    const Ts same_day{Trade(0, 2), Trade(2, 4)};
    CHECK_THROWS_AS(replay(plain, p, same_day), std::invalid_argument);  // sell and buy on day 2
    const Ts out_of_range{Trade(4, 6)};
    CHECK_THROWS_AS(replay(plain, p, out_of_range), std::invalid_argument);
}

TEST(tiny_tables_survive, "part4,edge") {
    for (int n = 0; n <= 3; ++n) {
        V p(static_cast<std::size_t>(n));
        for (int i = 0; i < n; ++i) p[static_cast<std::size_t>(i)] = i * 3 % 5;
        for (int k = 0; k <= 3; ++k)
            for (bool cd : {false, true}) {
                const Rules rules(k, 1, cd);
                CHECK_EQ(max_profit(rules, p), oracle(p, k, 1, cd));
                CHECK_EQ(plan(rules, p).profit, oracle(p, k, 1, cd));
            }
    }
}

TEST(million_days_unlimited_with_cooldown_and_fee, "part4,perf") {
    std::mt19937_64 r(0);
    const V p = walk(r, 1'000'000);
    const auto rules = Rules::unlimited().with_cooldown(true).with_fee(500);
    CHECK_WITHIN_MS(2000, CHECK_GE(max_profit(rules, p), 0););
}

TEST(plan_over_hundred_thousand_days, "part4,perf") {
    std::mt19937_64 r(0);
    const V p = walk(r, 100'000);
    const auto unlimited = Rules::unlimited().with_cooldown(true).with_fee(300);
    const Rules limited(20, 100, false);
    CHECK_WITHIN_MS(2000, {
        const Plan a1 = plan(unlimited, p);
        const Plan a2 = plan(limited, p);
        assert_valid_plan(unlimited, p, a1);
        assert_valid_plan(limited, p, a2);
        CHECK_EQ(replay(limited, p, a2.trades), a2.profit);
        CHECK(!a1.trades.empty());
    });
}

TEST(two_thousand_days_five_hundred_transactions, "part4,perf") {
    std::mt19937_64 r(7);
    const V p = walk(r, 2'000);
    const Rules rules(500, 0, true);
    CHECK_WITHIN_MS(2000, CHECK_GE(plan(rules, p).profit, 0););
}

// ================================================ C++-only edge cases (tag "cpp")

TEST(empty_input_never_wraps_around, "cpp,edge") {
    // `for (i = 0; i < p.size() - 1; ++i)` on an empty span: size() - 1 is SIZE_MAX, and the loop reads far out of bounds.
    const V empty;
    CHECK_EQ(max_profit_brute(empty), 0);
    CHECK_EQ(max_profit_once(empty), 0);
    CHECK_EQ(max_profit_unlimited(empty), 0);
    CHECK_EQ(max_profit_at_most(5, empty), 0);
    CHECK_EQ(max_profit(Rules::unlimited().with_cooldown(true), empty), 0);
    CHECK_EQ(plan(Rules::at_most(3), empty), (Plan{0, {}}));
    const Ts none;
    CHECK_EQ(replay(Rules::unlimited(), empty, none), 0);
}

TEST(sentinel_arithmetic_stays_inside_long_long, "cpp,edge") {
    // Unreachable states hold a large negative sentinel; adding a price or subtracting a fee to LLONG_MIN would be signed
    // overflow (UB, and UBSan aborts).  Extreme fee and extreme prices, with and without cooldown, bounded and unbounded.
    const V zeros(40, 0);
    const V highs(40, MAX);
    V zigzag(40, 0);
    for (std::size_t i = 1; i < zigzag.size(); i += 2) zigzag[i] = MAX;
    for (bool cd : {false, true})
        for (int k : {1, 3, Rules::UNLIMITED}) {
            const Rules rules(k, MAX, cd);
            CHECK_EQ(max_profit(rules, zeros), 0);
            CHECK_EQ(max_profit(rules, highs), 0);
            CHECK_EQ(max_profit(rules, zigzag), 0);  // fee == biggest spread: net 0
            CHECK_EQ(plan(rules, zigzag), (Plan{0, {}}));
            const Rules cheap(k, 0, cd);
            CHECK_GT(max_profit(cheap, zigzag), 0);
        }
}

TEST(table_size_is_computed_in_64_bits, "cpp,edge") {
    // (n + 1) * (k + 1) = 100001 * 50000 ~ 5e9 does not fit in int: computing it as int is UB and may wrap to something small.
    const V p(100'000, 0);
    const auto refused = try_plan(Rules::at_most(49'999), p);
    CHECK(!refused.has_value());
    const auto fine = try_plan(Rules::at_most(100), p);  // 100001 * 101 ~ 1e7 cells: fits
    REQUIRE(fine.has_value());
    CHECK_EQ(fine->profit, 0);
    const auto unlimited = try_plan(Rules::unlimited(), p);
    CHECK(unlimited.has_value());
}

TEST(try_plan_returns_optional_instead_of_throwing, "cpp") {
    const auto ok = try_plan(Rules::unlimited(), a(1, 3, 2, 8));
    REQUIRE(ok.has_value());
    CHECK_EQ(ok->profit, 8);
    const auto none = try_plan(Rules::at_most(60'000), V(130'000, 5));
    CHECK(!none.has_value());
    CHECK_THROWS_AS(plan(Rules::at_most(60'000), V(130'000, 5)), std::invalid_argument);
    CHECK_THROWS_AS(try_plan(Rules::unlimited(), a(1, -2)), std::invalid_argument);  // invalid input is still an exception
}

TEST(input_is_never_modified, "cpp") {
    std::mt19937_64 r(11);
    const V original = random_prices(r, 60, 40);
    const V copy = original;
    max_profit_brute(original);
    max_profit_once(original);
    max_profit_unlimited(original);
    max_profit_at_most(3, original);
    const Rules rules(3, 1, true);
    const Plan pl = plan(rules, original);
    replay(rules, original, pl.trades);
    CHECK_EQ(original, copy);
}

TEST(any_contiguous_container_converts_to_prices, "cpp") {
    const std::array<long long, 6> arr{7, 1, 5, 3, 6, 4};
    const long long raw[] = {7, 1, 5, 3, 6, 4};
    const V vec(std::begin(raw), std::end(raw));
    CHECK_EQ(max_profit_unlimited(arr), 7);
    CHECK_EQ(max_profit_unlimited(raw), 7);
    CHECK_EQ(max_profit_unlimited(vec), 7);
    CHECK_EQ(max_profit_unlimited(Prices(vec).subspan(1, 4)), 7);  // a sub-view [1,5,3,6]: (5-1) + (6-3)
    CHECK_EQ(max_profit_once(Prices(raw).first(0)), 0);
}

TEST(too_many_days_is_rejected, "cpp,edge") {
    const V ok(static_cast<std::size_t>(MAX_DAYS), 0);
    CHECK_EQ(max_profit_once(ok), 0);
    const V too_many(static_cast<std::size_t>(MAX_DAYS) + 1, 0);
    CHECK_THROWS_AS(max_profit_once(too_many), std::invalid_argument);
    CHECK_THROWS_AS(max_profit_unlimited(too_many), std::invalid_argument);
}

TEST(a_bad_price_anywhere_is_found, "cpp,edge") {
    V p(1000, 5);
    p.back() = MAX + 1;
    CHECK_THROWS_AS(max_profit_unlimited(p), std::invalid_argument);
    CHECK_THROWS_AS(max_profit_at_most(2, p), std::invalid_argument);
    CHECK_THROWS_AS(max_profit(Rules::unlimited(), p), std::invalid_argument);
    CHECK_THROWS_AS(plan(Rules::unlimited(), p), std::invalid_argument);
    CHECK_THROWS_AS(replay(Rules::unlimited(), p, {}), std::invalid_argument);
}

TEST(enum_values_outside_the_enumerators_do_not_crash, "cpp,edge") {
    // An enum class may hold any integer via static_cast.  The transitions must reject it (or leave it alone), not index a table with it.
    const auto bogus = static_cast<State>(7);
    CHECK_THROWS_AS(after_buy(bogus), IllegalState);
    CHECK_THROWS_AS(after_sell(bogus, Rules::unlimited()), IllegalState);
    CHECK_EQ(after_rest(bogus), bogus);
}

TEST(constructors_enforce_the_invariants, "cpp,edge") {
    CHECK_THROWS_AS(Trade(-1, 2), std::invalid_argument);
    CHECK_THROWS_AS(Trade(2, 2), std::invalid_argument);
    CHECK_THROWS_AS(Trade(3, 2), std::invalid_argument);
    CHECK_NOTHROW(Trade(0, 1));
    CHECK_THROWS_AS(Rules(-1, 0, false), std::invalid_argument);
    // IllegalState is a std::logic_error but not a std::invalid_argument (the two are different mistakes).
    bool caught_as_invalid_argument = false;
    try { after_buy(State::HOLD); } catch (const std::invalid_argument&) { caught_as_invalid_argument = true; } catch (const IllegalState&) {}
    CHECK(!caught_as_invalid_argument);
}

TEST(replay_with_extreme_prices_and_fee, "cpp,edge") {
    const V p = a(0, MAX, 0, 0, MAX);
    const Ts two{Trade(0, 1), Trade(3, 4)};  // legal even with a cooldown: sell day 1, buy day 3
    CHECK_EQ(replay(Rules::unlimited(), p, two), 2 * MAX);
    CHECK_EQ(replay(Rules::unlimited().with_fee(MAX), p, two), 0);
    CHECK_EQ(replay(Rules::unlimited().with_fee(MAX).with_cooldown(true), p, two), 0);
    const V low = a(0, 0);
    const Ts one{Trade(0, 1)};
    CHECK_EQ(replay(Rules::unlimited().with_fee(MAX), low, one), -MAX);  // replay does not require a profitable plan
}

MT_MAIN()
