// hc14 · Trade log -> VWAP — C++20 tests.  Same cases as test/TradeLogTest.java, RollingVwapTest.java and FastLogTest.java
// plus C++-only edge cases (tag "cpp"): string_views that end exactly at the buffer end (no NUL terminator to hide an
// over-read), signed chars >= 0x80 and embedded NULs, move-only-free value types, allocation counts of analyze_fast.
#include <algorithm>
#include <atomic>
#include <climits>
#include <cstdlib>
#include <iostream>
#include <map>
#include <new>
#include <random>
#include <type_traits>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace tradelog;
using namespace std::string_view_literals;

// ---------------------------------------------------------------- global allocation counter (test infrastructure)
namespace {
std::atomic<std::size_t> g_news{0};
struct AllocCount {
    std::size_t start = g_news.load();
    std::size_t get() const { return g_news.load() - start; }
};
}  // namespace
void* operator new(std::size_t n) {
    g_news.fetch_add(1, std::memory_order_relaxed);
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

// ---------------------------------------------------------------- printing for failure messages
namespace tradelog {
std::ostream& operator<<(std::ostream& os, const Trade& t) {
    return os << "Trade{" << t.ts_ms << "," << t.symbol << "," << t.price << "x" << t.qty << "}";
}
std::ostream& operator<<(std::ostream& os, const SymbolStats& s) {
    return os << "Stats{" << s.symbol << " n=" << s.count << " vol=" << s.volume << " notional=" << s.notional << " vwap=" << s.vwap
              << " min=" << s.min_price << " max=" << s.max_price << "}";
}
std::ostream& operator<<(std::ostream& os, const Report& r) {
    os << "Report{accepted=" << r.accepted << " malformed=" << r.malformed << " [";
    for (const auto& s : r.symbols) os << s << ";";
    return os << "]}";
}
std::ostream& operator<<(std::ostream& os, const SymbolNotional& s) { return os << s.symbol << "=" << s.notional; }
}  // namespace tradelog

namespace {

using Strs = std::vector<std::string>;
using Tops = std::vector<SymbolNotional>;

Trade T(long long ts, const char* sym, long long price, long long qty) { return Trade(ts, sym, price, qty); }
SymbolNotional SN(const char* s, long long n) { return SymbolNotional{s, n}; }

const char* const SAMPLE =
    "1000,AAPL,187.25,100\n"
    "1500,MSFT,410.5,50\n"
    "2000,AAPL,187.3,300\n"
    "oops\n"
    "2500,AAPL,187,100\n"
    "\n"
    "3000,msft,410.0,10\n"
    "3500,MSFT,410.5000,150\n"
    "4000,AAPL,187.25,0\n"
    "4500,AAPL,187.2501,400\n";

/// Like Java's text.split("\n", -1): keeps empty pieces, including the one after a trailing newline.
Strs lines(const std::string& text) {
    Strs out;
    std::size_t from = 0;
    while (true) {
        const auto nl = text.find('\n', from);
        if (nl == std::string::npos) {
            out.push_back(text.substr(from));
            return out;
        }
        out.push_back(text.substr(from, nl - from));
        from = nl + 1;
    }
}

Report slow(const std::string& text) { return analyze(lines(text)); }

void same(const std::string& text) {
    const Report a = slow(text), b = analyze_fast(text);
    CHECK_EQ(a, b, "text: " + text.substr(0, 120));
}

/// A string_view over a heap block that ends exactly at the view's end: an over-read is an ASan error, not a lucky NUL.
struct ExactBuf {
    std::vector<char> bytes;
    explicit ExactBuf(std::string_view s) : bytes(s.begin(), s.end()) { bytes.shrink_to_fit(); }
    std::string_view view() const { return {bytes.data(), bytes.size()}; }
};

// ================================================================================================ Part 1
TEST(parse_price_fixed_point, "part1") {
    CHECK_EQ(parse_price("187"), std::optional<long long>(1'870'000));
    CHECK_EQ(parse_price("187.25"), std::optional<long long>(1'872'500));
    CHECK_EQ(parse_price("187.3"), std::optional<long long>(1'873'000));
    CHECK_EQ(parse_price("187.2501"), std::optional<long long>(1'872'501));
    CHECK_EQ(parse_price("0.0001"), std::optional<long long>(1));
    CHECK_EQ(parse_price("0.5"), std::optional<long long>(5'000));
    CHECK_EQ(parse_price("007.5"), std::optional<long long>(75'000));
    CHECK_EQ(parse_price("999999999.9999"), std::optional<long long>(9'999'999'999'999LL));
}

TEST(parse_price_rejects, "part1,edge") {
    for (const char* s : {"", ".", ".5", "5.", "0", "0.0", "0.0000", "00", "-1", "+1", "-0.5", "1.23456", "1e3", "1E3", " 1", "1 ", "1..2",
                          "1.2.3", "1,5", "1234567890", "1234567890.5", "abc", "0x10", "NaN", "\xD9\xA3\xD9\xA4", "1.\xD9\xA3"}) {
        CHECK(!parse_price(s).has_value(), std::string("should be malformed: [") + s + "]");
    }
}

TEST(parse_line_valid, "part1") {
    CHECK_EQ(parse_line("1000,AAPL,187.25,100"), std::optional<Trade>(T(1000, "AAPL", 1'872'500, 100)));
    CHECK_EQ(parse_line("0,BRK.B,400,1"), std::optional<Trade>(T(0, "BRK.B", 4'000'000, 1)));
    CHECK_EQ(parse_line("007,A1,0.0001,999999999999"), std::optional<Trade>(T(7, "A1", 1, 999'999'999'999LL)));
    CHECK_EQ(parse_line("1000,AAPL,187.25,100")->notional(), 1'872'500LL * 100);
}

TEST(parse_line_malformed, "part1,edge") {
    for (const char* line : {
             "oops", ",,,", "1,AAPL,1", "1,AAPL,1,1,", "1,AAPL,1,1,1", "1,AAPL,1,", ",AAPL,1,1", "1,,1,1", "1,AAPL,,1",
             "1,aapl,1,1", "1,AA PL,1,1", "1,AAPL ,1,1", "1, AAPL,1,1", "1,AAPL-B,1,1", "1,AAPL_B,1,1", "1,AAPLMSFT123,1,1",
             "-1,AAPL,1,1", "+1,AAPL,1,1", "1.5,AAPL,1,1", "x,AAPL,1,1", "1234567890123456789,AAPL,1,1", " 1,AAPL,1,1",
             "1,AAPL,0,1", "1,AAPL,0.0000,1", "1,AAPL,-1,1", "1,AAPL,1.00001,1", "1,AAPL,.5,1", "1,AAPL,1.,1", "1,AAPL,1e2,1",
             "1,AAPL,1,0", "1,AAPL,1,-1", "1,AAPL,1,1.5", "1,AAPL,1,1 ", "1,AAPL,1,1\r", "1,AAPL,1,1000000000000", "1,AAPL,1,abc",
             "1,AAPL,100000000.0000,10000000",  // price * qty = 1e19 > LLONG_MAX
             "1,AAPL,303700.0500,3037000500"}) {  // 3037000500^2 just overflows
        CHECK(!parse_line(line).has_value(), std::string("should be malformed: [") + line + "]");
    }
}

TEST(field_length_boundaries, "part1,edge") {
    CHECK(parse_line("999999999999999999,A,1,1").has_value());  // 18-digit timestamp
    CHECK(!parse_line("1000000000000000000,A,1,1").has_value());  // 19
    CHECK(parse_line("1,ABCDEFGHIJ,1,1").has_value());  // 10-character symbol
    CHECK(!parse_line("1,ABCDEFGHIJK,1,1").has_value());  // 11
    CHECK(parse_line("1,A,999999999.9999,1").has_value());
    CHECK(!parse_line("1,A,1000000000,1").has_value());  // 10 integer digits
    CHECK(parse_line("1,A,1,999999999999").has_value());  // 12-digit quantity
    CHECK(!parse_line("1,A,1,1000000000000").has_value());  // 13
    // 3037000499^2 < LLONG_MAX < 3037000500^2
    CHECK(parse_line("1,A,303700.0499,3037000499").has_value());
    CHECK_EQ(parse_line("1,A,303700.0499,3037000499")->notional(), 3037000499LL * 3037000499LL);
}

TEST(only_ascii_digits_count, "part1,edge") {
    CHECK(!parse_line("\xD9\xA1\xD9\xA2,AAPL,1,1").has_value());  // UTF-8 Arabic-Indic digits
    CHECK(!parse_line("1,AAPL,1,\xD9\xA3").has_value());
    CHECK(!parse_line("1,\xEF\xBC\xA1\xEF\xBC\xA1,1,1").has_value());  // fullwidth letters
}

TEST(trade_constructor_validates, "part1,edge") {
    CHECK_THROWS_AS(Trade(-1, "A", 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(Trade(0, "a", 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(Trade(0, "A", 0, 1), std::invalid_argument);
    CHECK_THROWS_AS(Trade(0, "A", 1, 0), std::invalid_argument);
    CHECK_THROWS_AS(Trade(0, "A", LLONG_MAX, 2), std::overflow_error);
}

TEST(vwap_rounds_half_up, "part1") {
    CHECK_EQ(vwap(5, 2), 3LL);  // 2.5 -> 3
    CHECK_EQ(vwap(4, 2), 2LL);
    CHECK_EQ(vwap(1, 3), 0LL);
    CHECK_EQ(vwap(2, 3), 1LL);
    CHECK_EQ(vwap(1, 2), 1LL);  // 0.5 -> 1
    CHECK_EQ(vwap(1'685'150'400LL, 900), 1'872'389LL);
    CHECK_EQ(vwap(1'685'150'400LL + 400, 900), 1'872'390LL);
}

TEST(vwap_never_overflows, "part1,edge") {
    CHECK_EQ(vwap(LLONG_MAX, 1), LLONG_MAX);
    CHECK_EQ(vwap(LLONG_MAX, 2), 4'611'686'018'427'387'904LL);  // 2^62 - 0.5 -> 2^62; a "2 * r" rounding test overflows here
    CHECK_EQ(vwap(LLONG_MAX, LLONG_MAX), 1LL);
    CHECK_EQ(vwap(LLONG_MAX / 2 + 1, LLONG_MAX), 1LL);  // just over 0.5
    CHECK_EQ(vwap(LLONG_MAX / 2, LLONG_MAX), 0LL);  // just under
    CHECK_THROWS_AS(vwap(5, 0), std::invalid_argument);
    CHECK_THROWS_AS(vwap(5, -1), std::invalid_argument);
    CHECK_THROWS_AS(vwap(-5, 1), std::invalid_argument);
}

TEST(analyze_sample, "part1") {
    const Report r = analyze(lines(SAMPLE));
    CHECK_EQ(r.accepted, 6LL);
    CHECK_EQ(r.malformed, 3LL);  // oops, lowercase msft, qty 0; the empty line is not counted
    const std::vector<SymbolStats> want = {
        {"AAPL", 4, 900, 1'685'150'400LL, 1'872'389, 1'870'000, 1'873'000},
        {"MSFT", 2, 200, 821'000'000LL, 4'105'000, 4'105'000, 4'105'000}};
    CHECK_EQ(r.symbols, want);
}

TEST(render_sample, "part1,fmt") {
    const Strs want = {"AAPL count=4 volume=900 notional=168515.0400 vwap=187.2389 min=187.0000 max=187.3000",
                       "MSFT count=2 volume=200 notional=82100.0000 vwap=410.5000 min=410.5000 max=410.5000",
                       "accepted=6 malformed=3"};
    CHECK_EQ(render(analyze(lines(SAMPLE))), want);
}

TEST(format_price_cases, "part1,fmt") {
    CHECK_EQ(format_price(0), std::string("0.0000"));
    CHECK_EQ(format_price(1), std::string("0.0001"));
    CHECK_EQ(format_price(5'000), std::string("0.5000"));
    CHECK_EQ(format_price(1'872'500), std::string("187.2500"));
    CHECK_EQ(format_price(9'999'999'999'999LL), std::string("999999999.9999"));
    CHECK_EQ(format_price(LLONG_MAX), std::string("922337203685477.5807"));
    CHECK_THROWS_AS(format_price(-1), std::invalid_argument);
    for (long long u : {1LL, 10LL, 99'999LL, 1'872'500LL, 9'999'999'999'999LL}) CHECK_EQ(parse_price(format_price(u)), std::optional<long long>(u));
}

TEST(empty_and_blank, "part1,edge") {
    const Report empty = analyze({});
    CHECK_EQ(empty, (Report{{}, 0, 0}));
    CHECK_EQ(render(empty), (Strs{"accepted=0 malformed=0"}));
    CHECK_EQ(analyze({"", "", ""}), (Report{{}, 0, 0}));
    CHECK_EQ(analyze({" ", "\t", "\r"}), (Report{{}, 0, 3}));  // whitespace-only is not empty: it is malformed
}

TEST(single_trade, "part1,edge") {
    const Report r = analyze({"5,X,2.5,4"});
    CHECK_EQ(r.symbols, (std::vector<SymbolStats>{{"X", 1, 4, 100'000, 25'000, 25'000, 25'000}}));
}

TEST(symbols_sorted_bytewise_and_time_order_irrelevant, "part1,edge") {
    const Report r = analyze({"9,AA,1,1", "3,A1,1,1", "7,A.B,1,1", "1,B,1,1", "8,AA,3,1"});
    std::vector<std::string> names;
    for (const auto& s : r.symbols) names.push_back(s.symbol);
    CHECK_EQ(names, (Strs{"A.B", "A1", "AA", "B"}));
    const SymbolStats& aa = r.symbols[2];
    CHECK_EQ(aa.count, 2LL);
    CHECK_EQ(aa.min_price, 10'000LL);
    CHECK_EQ(aa.max_price, 30'000LL);
    CHECK_EQ(aa.vwap, 20'000LL);
}

TEST(vwap_stays_inside_min_max, "part1,edge") {
    CHECK_EQ(analyze({"1,Q,0.0001,1", "2,Q,0.0002,2"}).symbols[0].vwap, 2LL);  // (1 + 4) / 3 = 1.67 -> 2
    CHECK_EQ(analyze({"1,Q,0.0001,1", "2,Q,0.0001,1"}).symbols[0].vwap, 1LL);
}

TEST(sum_overflow_throws, "part1,edge") {
    const std::string big = "1,BIG,100000000.0000,9000000";  // 1e12 * 9e6 = 9e18 fits in long long; two do not
    CHECK(parse_line(big).has_value());
    CHECK_EQ(parse_line(big)->notional(), 9'000'000'000'000'000'000LL);
    CHECK_EQ(analyze({big}).symbols.size(), 1u);
    CHECK_THROWS_AS(analyze({big, big}), std::overflow_error);
    CHECK_EQ(analyze({big, "2,BIG2,100000000.0000,9000000"}).symbols.size(), 2u);  // different symbols do not interact
    const Report bad = analyze({"1,BIG,100000000.0000,10000000", "2,OK,1,1"});  // one line's product overflows: malformed, no throw
    CHECK_EQ(bad.malformed, 1LL);
    CHECK_EQ(bad.accepted, 1LL);
}

TEST(views_end_exactly_at_the_buffer_end, "part1,edge,cpp") {
    // No NUL terminator after the view: a scanner that reads one char too far is an ASan report.
    for (std::string_view s : {"187.25"sv, "187"sv, "0.0001"sv, "5."sv, "."sv, "1.2345"sv}) {
        const ExactBuf b(s);
        (void)parse_price(b.view());
    }
    for (std::string_view s : {"1,A,1,1"sv, "1,A,1,"sv, "1,A,1"sv, "1,A,"sv, "1,A"sv, "1,"sv, "1"sv, ","sv, ",,,"sv, "1,A,1.,1"sv}) {
        const ExactBuf b(s);
        (void)parse_line(b.view());
    }
    CHECK(parse_line(ExactBuf("12,AB,3.5,7").view()).has_value());
    CHECK_EQ(parse_price(ExactBuf("187.25xyz").view().substr(0, 6)), std::optional<long long>(1'872'500));
}

TEST(high_bytes_and_embedded_nul, "part1,edge,cpp") {
    // char is signed on this platform: 0xE9 is negative, and a table lookup indexed by it is out of bounds.
    CHECK(!parse_line("1,A\xE9,1,1").has_value());
    CHECK(!parse_line("1,A,1\xE9,1").has_value());
    CHECK(!parse_line("\xFF" "1,A,1,1").has_value());
    CHECK(!valid_symbol("\x80"));
    const std::string nul_in_symbol("1,A\0B,1,1", 9);
    CHECK_EQ(nul_in_symbol.size(), 9u);
    CHECK(!parse_line(nul_in_symbol).has_value());
    const std::string nul_at_end("1,A,1,1\0", 8);
    CHECK(!parse_line(nul_at_end).has_value());
    CHECK_EQ(analyze({nul_in_symbol, nul_at_end, "1,A,1,1"}), (Report{{{"A", 1, 1, 10'000, 10'000, 10'000, 10'000}}, 1, 2}));
}

TEST(value_types, "part1,cpp") {
    static_assert(!std::is_default_constructible_v<Trade>, "an invalid Trade must not be constructible by accident");
    static_assert(std::is_copy_constructible_v<Trade> && std::is_nothrow_move_constructible_v<Trade>);
    Trade a = T(1, "A", 10'000, 2);
    Trade b = std::move(a);
    CHECK_EQ(b.symbol, std::string("A"));
    CHECK_EQ(b.notional(), 20'000LL);
}

// ================================================================================================ Part 2
RollingVwap sample_window() {
    RollingVwap r(1000);
    r.on_trade(T(0, "AAPL", 100'000, 10));
    r.on_trade(T(400, "AAPL", 120'000, 20));
    r.on_trade(T(900, "MSFT", 500'000, 5));
    return r;
}

using OL = std::optional<long long>;

TEST(sample_walkthrough, "part2") {
    RollingVwap r = sample_window();
    CHECK_EQ(r.vwap("AAPL", 900), OL(113'333));  // (1e6 + 2.4e6) / 30 = 113333.33
    CHECK_EQ(r.vwap("MSFT", 900), OL(500'000));
    CHECK_EQ(r.vwap("GOOG", 900), std::optional<long long>());
    r.on_trade(T(1000, "AAPL", 110'000, 10));  // the trade at t=0 expires exactly now
    CHECK_EQ(r.live_symbols(), 2u);
    CHECK_EQ(r.live_trades(), 3u);
    CHECK_EQ(r.volume("AAPL"), 30LL);
    CHECK_EQ(r.notional("AAPL"), 3'500'000LL);
    CHECK_EQ(r.vwap("AAPL", 1000), OL(116'667));
    CHECK_EQ(r.vwap("MSFT", 1900), std::optional<long long>());  // 1900 - 900 = 1000: expired, and the symbol disappears
    CHECK_EQ(r.live_symbols(), 1u);
    CHECK_EQ(r.now(), 1900LL);
}

TEST(expiry_boundary_is_half_open, "part2,edge") {
    RollingVwap r(10);
    r.on_trade(T(5, "A", 10'000, 1));
    CHECK_EQ(r.vwap("A", 14), OL(10'000));  // 14 - 5 = 9 < 10: live
    CHECK_EQ(r.live_trades(), 1u);
    CHECK_EQ(r.vwap("A", 15), std::optional<long long>());  // 10: expired
    CHECK_EQ(r.live_trades(), 0u);
    CHECK_EQ(r.live_symbols(), 0u);
}

TEST(window_one_keeps_only_the_same_timestamp, "part2,edge") {
    RollingVwap r(1);
    r.on_trade(T(5, "A", 10'000, 1));
    r.on_trade(T(5, "A", 30'000, 1));
    CHECK_EQ(r.vwap("A", 5), OL(20'000));
    r.on_trade(T(6, "A", 50'000, 1));
    CHECK_EQ(r.live_trades(), 1u);
    CHECK_EQ(r.vwap("A", 6), OL(50'000));
}

TEST(same_timestamp_trades_expire_together, "part2,edge") {
    RollingVwap r(100);
    for (int i = 0; i < 50; ++i) r.on_trade(T(7, "A", 10'000 + i, 2));
    CHECK_EQ(r.live_trades(), 50u);
    CHECK_EQ(r.volume("A"), 100LL);
    r.vwap("A", 106);
    CHECK_EQ(r.live_trades(), 50u);
    r.vwap("A", 107);
    CHECK_EQ(r.live_trades(), 0u);
    CHECK_EQ(r.volume("A"), 0LL);
}

TEST(time_never_goes_backwards, "part2,edge") {
    RollingVwap r(100);
    r.on_trade(T(50, "A", 10'000, 1));
    CHECK_THROWS_AS(r.on_trade(T(49, "A", 10'000, 1)), std::invalid_argument);
    CHECK_EQ(r.live_trades(), 1u);  // the rejected trade was not added
    CHECK_EQ(r.now(), 50LL);
    CHECK_THROWS_AS(r.vwap("A", 49), std::invalid_argument);
    r.on_trade(T(50, "A", 10'000, 1));  // the same instant is fine
    CHECK_EQ(r.vwap("A", 60), OL(10'000));
    CHECK_EQ(r.now(), 60LL);
    CHECK_THROWS_AS(r.on_trade(T(55, "A", 10'000, 1)), std::invalid_argument);  // the query already moved the clock to 60
}

TEST(constructor_and_empty_queries, "part2,edge") {
    CHECK_THROWS_AS(RollingVwap(0), std::invalid_argument);
    CHECK_THROWS_AS(RollingVwap(-5), std::invalid_argument);
    RollingVwap r(10);
    CHECK_EQ(r.now(), 0LL);
    CHECK_EQ(r.vwap("A", 0), std::optional<long long>());
    CHECK_EQ(r.volume("A"), 0LL);
    CHECK_EQ(r.notional("A"), 0LL);
}

TEST(symbols_are_independent, "part2,edge") {
    RollingVwap r(100);
    r.on_trade(T(0, "A", 10'000, 1));
    r.on_trade(T(60, "B", 20'000, 1));
    r.on_trade(T(120, "A", 30'000, 1));
    CHECK_EQ(r.vwap("A", 120), OL(30'000));  // the A at t=0 expired
    CHECK_EQ(r.vwap("B", 120), OL(20'000));
    CHECK_EQ(r.live_trades(), 2u);
}

TEST(overflow_rejects_the_trade_and_keeps_state, "part2,edge") {
    RollingVwap r(1000);
    r.on_trade(T(0, "BIG", 1'000'000'000'000LL, 9'000'000));  // notional 9e18
    CHECK_THROWS_AS(r.on_trade(T(1, "BIG", 1'000'000'000'000LL, 9'000'000)), std::overflow_error);
    CHECK_EQ(r.live_trades(), 1u);
    CHECK_EQ(r.notional("BIG"), 9'000'000'000'000'000'000LL);
    CHECK_EQ(r.volume("BIG"), 9'000'000LL);
    CHECK_EQ(r.vwap("BIG", 1), OL(1'000'000'000'000LL));
    r.on_trade(T(2, "OK", 10'000, 1));
    CHECK_EQ(r.live_trades(), 2u);
    r.on_trade(T(1000, "BIG", 1'000'000'000'000LL, 9'000'000));  // the old one has expired: fits again
    CHECK_EQ(r.notional("BIG"), 9'000'000'000'000'000'000LL);
}

TEST(quantity_overflow_also_rejects, "part2,edge") {
    RollingVwap r(1000);
    r.on_trade(T(0, "Q", 1, LLONG_MAX - 1));
    CHECK_THROWS_AS(r.on_trade(T(1, "Q", 1, 2)), std::overflow_error);
    CHECK_EQ(r.volume("Q"), LLONG_MAX - 1);
    CHECK_EQ(r.live_trades(), 1u);
    r.on_trade(T(2, "Q", 1, 1));
    CHECK_EQ(r.volume("Q"), LLONG_MAX);
}

TEST(window_vwap_rounds_half_up, "part2,edge") {
    RollingVwap r(1000);
    r.on_trade(T(0, "A", 1, 1));
    r.on_trade(T(1, "A", 2, 1));
    CHECK_EQ(r.vwap("A", 1), OL(2));  // 1.5 -> 2
    r.on_trade(T(2, "B", 1, 2));
    r.on_trade(T(2, "B", 2, 1));
    CHECK_EQ(r.vwap("B", 2), OL(1));  // 4 / 3 = 1.33
}

struct Model {  // obviously correct and slow
    std::vector<Trade> all;
    long long window;
    explicit Model(long long w) : window(w) {}
    OL vwap(const std::string& sym, long long now) const {
        long long vol = 0, not_ = 0;
        for (const auto& t : all) {
            if (t.symbol == sym && now - t.ts_ms < window) {
                vol += t.qty;
                not_ += t.notional();
            }
        }
        return vol == 0 ? OL() : OL(tradelog::vwap(not_, vol));
    }
    Tops top(int k, long long now) const {
        std::map<std::string, long long> m;
        for (const auto& t : all)
            if (now - t.ts_ms < window) m[t.symbol] += t.notional();
        Tops out;
        for (const auto& [s, n] : m) out.push_back({s, n});
        std::sort(out.begin(), out.end(), [](const SymbolNotional& a, const SymbolNotional& b) {
            return a.notional != b.notional ? a.notional > b.notional : a.symbol < b.symbol;
        });
        if (out.size() > static_cast<std::size_t>(k)) out.resize(static_cast<std::size_t>(k));
        return out;
    }
};

TEST(random_vwap_matches_brute_force, "part2") {
    std::mt19937 rnd(7);
    const char* syms[] = {"A", "B", "C", "D.E", "F1"};
    for (long long window : {1LL, 3LL, 50LL, 1000LL}) {
        RollingVwap fast(window);
        Model model(window);
        long long now = 0;
        for (int i = 0; i < 3000; ++i) {
            if (rnd() % 4 == 0) now += static_cast<long long>(rnd() % 30);
            const Trade tr = T(now, syms[rnd() % 5], 1 + static_cast<long long>(rnd() % 2'000'000), 1 + static_cast<long long>(rnd() % 500));
            fast.on_trade(tr);
            model.all.push_back(tr);
            if (i % 3 == 0) {
                const std::string q = syms[rnd() % 5];
                CHECK_EQ(fast.vwap(q, now), model.vwap(q, now), "window " + std::to_string(window) + " step " + std::to_string(i));
            }
        }
    }
}

TEST(amortised_constant_time_per_trade, "part2,perf") {
    // 100k trades stay live; asking for a VWAP after every trade must not rescan the window (that would be 1e11 steps)
    std::mt19937 rnd(0);
    RollingVwap r(100'000);
    std::vector<std::string> syms;
    for (int i = 0; i < 500; ++i) syms.push_back("S" + std::to_string(i));
    long long check = 0;
    CHECK_WITHIN_MS(3000, {
        for (int i = 0; i < 1'000'000; ++i) {
            r.on_trade(T(i, syms[rnd() % 500].c_str(), 10'000 + static_cast<long long>(rnd() % 1'000'000), 1 + static_cast<long long>(rnd() % 1000)));
            check += r.vwap(syms[static_cast<std::size_t>(i) % 500], i).value_or(0);
        }
    });
    CHECK(check > 0);
    CHECK_EQ(r.live_trades(), 100'000u);
}

// ================================================================================================ Part 3
TEST(top_k_basic, "part3") {
    RollingVwap r = sample_window();  // AAPL 3'400'000, MSFT 2'500'000
    CHECK_EQ(r.top_k(5, 900), (Tops{SN("AAPL", 3'400'000), SN("MSFT", 2'500'000)}));
    CHECK_EQ(r.top_k(1, 900), (Tops{SN("AAPL", 3'400'000)}));
    CHECK_EQ(r.top_k(0, 900), Tops{});
    CHECK_EQ(r.top_k(2, 1000), (Tops{SN("MSFT", 2'500'000), SN("AAPL", 2'400'000)}));  // AAPL's t=0 trade expired
    CHECK_EQ(r.now(), 1000LL);
    CHECK_EQ(r.top_k(10, 1400), (Tops{SN("MSFT", 2'500'000)}));  // AAPL's t=400 trade expires at 1400
    CHECK_EQ(r.top_k(10, 1900), Tops{});
}

TEST(top_k_ties_break_by_symbol_ascending, "part3,edge") {
    RollingVwap r(1000);
    for (const char* s : {"ZED", "ABC", "MID", "A.B"}) r.on_trade(T(0, s, 10'000, 3));
    r.on_trade(T(0, "TOP", 10'000, 4));
    CHECK_EQ(r.top_k(3, 0), (Tops{SN("TOP", 40'000), SN("A.B", 30'000), SN("ABC", 30'000)}));
    CHECK_EQ(r.top_k(99, 0), (Tops{SN("TOP", 40'000), SN("A.B", 30'000), SN("ABC", 30'000), SN("MID", 30'000), SN("ZED", 30'000)}));
}

TEST(top_k_arguments_and_clock, "part3,edge") {
    RollingVwap r(10);
    CHECK_EQ(r.top_k(3, 0), Tops{});
    CHECK_THROWS_AS(r.top_k(-1, 0), std::invalid_argument);
    r.on_trade(T(5, "A", 10'000, 1));
    CHECK_THROWS_AS(r.top_k(1, 4), std::invalid_argument);  // time went backwards
    CHECK_THROWS_AS(r.top_k(-1, 4), std::invalid_argument);  // k is checked first
    CHECK_EQ(r.top_k(0, 4 + 100), Tops{});  // k = 0 still advances the clock (and expires A)
    CHECK_EQ(r.live_trades(), 0u);
}

TEST(top_k_returns_an_independent_snapshot, "part3,edge,cpp") {
    RollingVwap r = sample_window();
    const Tops top = r.top_k(2, 900);
    r.on_trade(T(901, "MSFT", 500'000, 100));
    CHECK_EQ(top, (Tops{SN("AAPL", 3'400'000), SN("MSFT", 2'500'000)}));  // a later trade does not change the earlier answer
    CHECK_EQ(r.top_k(1, 901)[0], SN("MSFT", 52'500'000));
}

TEST(top_k_with_huge_k_is_clamped, "part3,edge,cpp") {
    RollingVwap r(10);
    r.on_trade(T(0, "A", 1, 1));
    CHECK_EQ(r.top_k(INT_MAX, 0), (Tops{SN("A", 1)}));  // k is clamped, not used as a size_t reserve
}

TEST(random_top_k_matches_brute_force, "part3") {
    std::mt19937 rnd(11);
    std::vector<std::string> syms;
    for (int i = 0; i < 12; ++i) syms.push_back(std::string("S") + static_cast<char>('A' + i));
    for (long long window : {2LL, 40LL, 500LL}) {
        RollingVwap fast(window);
        Model model(window);
        long long now = 0;
        for (int i = 0; i < 2000; ++i) {
            now += static_cast<long long>(rnd() % 3);
            const Trade tr = T(now, syms[rnd() % 12].c_str(), 1 + static_cast<long long>(rnd() % 5), 1 + static_cast<long long>(rnd() % 4));  // tiny numbers: many ties
            fast.on_trade(tr);
            model.all.push_back(tr);
            if (i % 5 == 0) {
                const int k = static_cast<int>(rnd() % 14);
                CHECK_EQ(fast.top_k(k, now), model.top(k, now), "window " + std::to_string(window) + " step " + std::to_string(i));
            }
        }
    }
}

TEST(top_k_over_many_symbols, "part3,perf") {
    std::mt19937 rnd(1);
    RollingVwap r(50'000);
    std::vector<std::string> syms;
    for (int i = 0; i < 5000; ++i) syms.push_back("T" + std::to_string(i));
    long long total = 0;
    CHECK_WITHIN_MS(3000, {
        for (int i = 0; i < 500'000; ++i) {
            r.on_trade(T(i, syms[rnd() % 5000].c_str(), 10'000 + static_cast<long long>(rnd() % 100'000), 1 + static_cast<long long>(rnd() % 100)));
            if (i % 500 == 0) total += static_cast<long long>(r.top_k(10, i).size());
        }
    });
    CHECK(total > 9'900 && total <= 10'000, "total " + std::to_string(total));
}

// ================================================================================================ Part 4
TEST(fast_sample_matches_string_version, "part4") {
    const std::string text = SAMPLE;
    const Report r = analyze_fast(text);
    CHECK_EQ(r.accepted, 6LL);
    CHECK_EQ(r.malformed, 3LL);
    CHECK_EQ(r, analyze(lines(text)));
    CHECK_EQ(r.symbols[0].vwap, 1'872'389LL);
}

TEST(fast_empty_and_blank, "part4,edge") {
    CHECK_EQ(analyze_fast(""), (Report{{}, 0, 0}));
    CHECK_EQ(analyze_fast("\n\n\n"), (Report{{}, 0, 0}));
    same("");
    same("\n");
    same(" \n\t\n\r\n");  // whitespace-only lines are malformed
}

TEST(fast_last_line_without_newline, "part4,edge") {
    same("1,A,1,1\n2,A,3,1");
    same("1,A,1,1\n2,A,3,1\n");
    same("1,A,1,1\n\n\n2,A,3,1\n\n");
    CHECK_EQ(analyze_fast("1,A,1,1\n2,A,3,1").accepted, 2LL);
}

TEST(fast_every_malformed_class_agrees, "part4,edge") {
    const Strs bad = {"oops", ",,,", "1,AAPL,1", "1,AAPL,1,1,", "1,AAPL,1,1,1", "1,AAPL,1,", ",AAPL,1,1", "1,,1,1", "1,AAPL,,1",
                      "1,aapl,1,1", "1,AA PL,1,1", "1,AAPL ,1,1", "1,AAPL-B,1,1", "1,AAPLMSFT123,1,1", "-1,AAPL,1,1", "+1,AAPL,1,1",
                      "1.5,AAPL,1,1", "1234567890123456789,AAPL,1,1", "1,AAPL,0,1", "1,AAPL,0.0000,1", "1,AAPL,-1,1", "1,AAPL,1.00001,1",
                      "1,AAPL,.5,1", "1,AAPL,1.,1", "1,AAPL,1e2,1", "1,AAPL,1,0", "1,AAPL,1,-1", "1,AAPL,1,1.5", "1,AAPL,1,1\r",
                      "1,AAPL,1,1000000000000", "1,AAPL,1234567890,1", "1,AAPL,100000000.0000,10000000", "1,AAPL,303700.0500,3037000500"};
    for (const auto& line : bad) CHECK_EQ(analyze_fast(line), (Report{{}, 0, 1}), "should be malformed: [" + line + "]");
    const Strs good = {"0,A,1,1", "999999999999999999,A,1,1", "1,ABCDEFGHIJ,1,1", "1,A.B.C,1,1", "1,A,999999999.9999,1",
                       "1,A,0.0001,999999999999", "007,A,007.5,0001", "1,BIG,303700.0499,3037000499", "1,A,5.5000,1"};
    for (const auto& line : good) CHECK_EQ(analyze_fast(line).accepted, 1LL, "should be valid: [" + line + "]");
    std::string all;
    for (const auto& l : bad) all += l + "\n";
    for (const auto& l : good) all += l + "\n";
    same(all);
}

TEST(fast_high_bytes_and_nul_are_malformed_not_crashes, "part4,edge,cpp") {
    // char is signed: a table indexed by the raw byte would read before the array for 0xE9
    std::string data = "1,A\xE9,1,1\n1,B,1,1\n";
    data.push_back('\0');
    data += "\n\xFF\x80\n1,C,1,1";
    data.push_back('\0');
    const Report r = analyze_fast(data);
    CHECK_EQ(r.accepted, 1LL);
    CHECK_EQ(r.malformed, 4LL);
    CHECK_EQ(r.symbols[0].symbol, std::string("B"));
    same(data);
    const ExactBuf b(data);  // and a view that ends exactly at the end of its allocation
    CHECK_EQ(analyze_fast(b.view()), r);
}

TEST(fast_overflow_behaves_like_the_string_version, "part4,edge") {
    const std::string big = "1,BIG,100000000.0000,9000000";
    CHECK_THROWS_AS(analyze_fast(big + "\n" + big), std::overflow_error);
    CHECK_THROWS_AS(analyze(lines(big + "\n" + big)), std::overflow_error);
    same(big + "\n2,BIG2,100000000.0000,9000000");
    same("1,BIG,100000000.0000,10000000\n2,OK,1,1");
}

std::string symbol_of(int n) {
    const std::string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.";
    std::string s;
    do {
        s.push_back(alphabet[static_cast<std::size_t>(n % 37)]);
        n /= 37;
    } while (n > 0);
    return s;
}

TEST(fast_table_grows_and_keeps_every_symbol, "part4,edge") {
    std::string text;
    for (int i = 0; i < 30'000; ++i)
        text += std::to_string(i) + "," + symbol_of(i) + "," + std::to_string(1 + i % 50) + "." + std::to_string(i % 7) + "," + std::to_string(1 + i % 9) + "\n";
    text += "5,ZZZZZZZZZZ,1,1\n5,9999999999,1,1\n5,..........,1,1\n";  // ten characters: all 60 bits in use
    same(text);
    CHECK_EQ(analyze_fast(text).symbols.size(), 30'003u);
}

TEST(fast_fuzz_matches_string_version, "part4") {
    std::mt19937 rnd(42);
    const std::string junk = ",.0123456789ABCz- \r+eE\xE9";
    for (int round = 0; round < 40; ++round) {
        std::string text;
        for (int i = 0; i < 500; ++i) {
            std::string line = std::to_string(rnd() % 100'000) + "," + symbol_of(static_cast<int>(rnd() % 60)) + "," + std::to_string(rnd() % 1000) + "." +
                               std::to_string(rnd() % 10'000) + "," + std::to_string(rnd() % 5'000);
            const int edits = static_cast<int>(rnd() % 3);
            for (int e = 0; e < edits && !line.empty(); ++e) {
                const std::size_t at = rnd() % line.size();
                switch (rnd() % 3) {
                    case 0: line.erase(at, 1); break;
                    case 1: line[at] = junk[rnd() % junk.size()]; break;
                    default: line.insert(line.begin() + static_cast<std::ptrdiff_t>(at), junk[rnd() % junk.size()]); break;
                }
            }
            text += line + (rnd() % 30 == 0 ? "\n\n" : "\n");
        }
        same(text);
    }
}

struct Gen {
    std::string data;
    long long accepted = 0, malformed = 0, volume = 0, notional = 0;
};

/// n lines over symbol_count symbols, about 1% malformed; the expected totals are tracked the direct way.
Gen generate(int n, int symbol_count, unsigned seed) {
    std::mt19937 rnd(seed);
    std::vector<std::string> syms;
    for (int i = 0; i < symbol_count; ++i) syms.push_back(symbol_of(i * 7919 + 13));
    Gen g;
    g.data.reserve(static_cast<std::size_t>(n) * 36);
    for (int i = 0; i < n; ++i) {
        const int whole = 1 + static_cast<int>(rnd() % 999), digits = static_cast<int>(rnd() % 5);
        int pow10 = 1;
        for (int d = 0; d < digits; ++d) pow10 *= 10;
        const int frac = digits == 0 ? 0 : static_cast<int>(rnd() % static_cast<unsigned>(pow10));
        const long long qty = 1 + static_cast<long long>(rnd() % 5000);
        std::string price = std::to_string(whole);
        if (digits > 0) {
            std::string f = std::to_string(frac);
            price += "." + std::string(static_cast<std::size_t>(digits) - f.size(), '0') + f;
        }
        const long long units = whole * 10'000LL + (digits == 0 ? 0 : frac * (10'000LL / pow10));
        g.data += std::to_string(1'700'000'000'000LL + i);
        g.data += ',';
        g.data += syms[rnd() % static_cast<unsigned>(symbol_count)];
        g.data += ',';
        if (rnd() % 100 == 0) {
            g.data += (rnd() % 2 ? "x" + price + "," + std::to_string(qty) : price + ",0");
            g.data += '\n';
            ++g.malformed;
            continue;
        }
        g.data += price + "," + std::to_string(qty) + "\n";
        ++g.accepted;
        g.volume += qty;
        g.notional += units * qty;
    }
    return g;
}

TEST(fast_does_not_allocate_per_line, "part4,cpp") {
    const Gen g = generate(100'000, 2000, 5);
    analyze_fast(g.data);  // warm-up has no effect on allocation counts, but keeps the measurement honest
    const AllocCount a;
    const Report r = analyze_fast(g.data);
    // hash-table growth, the result vector: a few dozen.  One String per line would be >= 100'000.
    CHECK(a.get() < 200u, "allocations: " + std::to_string(a.get()));
    CHECK_EQ(r.accepted, g.accepted);
    CHECK_EQ(r.symbols.size(), 2000u);
}

TEST(fast_one_million_lines, "part4,perf") {
    const Gen g = generate(1'000'000, 2000, 5);
    CHECK(g.data.size() > 30'000'000u, "input should be ~35 MB, got " + std::to_string(g.data.size()));
    const Gen warm = generate(200'000, 2000, 1);
    analyze_fast(warm.data);
    Report r{{}, 0, 0};
    CHECK_WITHIN_MS(1000, { r = analyze_fast(g.data); });
    CHECK_EQ(r.accepted, g.accepted);
    CHECK_EQ(r.malformed, g.malformed);
    long long vol = 0, not_ = 0;
    for (const auto& s : r.symbols) {
        vol += s.volume;
        not_ += s.notional;
    }
    CHECK_EQ(vol, g.volume);
    CHECK_EQ(not_, g.notional);
    CHECK_EQ(r.symbols.size(), 2000u);
}

TEST(fast_agrees_on_a_large_input, "part4,perf") {
    const Gen g = generate(200'000, 500, 9);
    CHECK_EQ(slow(g.data), analyze_fast(g.data));
}

}  // namespace

MT_MAIN()
