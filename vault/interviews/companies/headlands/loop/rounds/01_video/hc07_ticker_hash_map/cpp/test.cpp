// hc07 · Ticker hash map — C++20 tests.  Same cases as the Java test/*.java plus C++-only edge cases (tag "cpp"):
// string_view lookups and small-string keys allocate nothing, std::hash pitfalls, NUL inside a string_view, `char` signedness,
// the -1 -> UINT64_MAX conversion trap, `off + 8` wrap-around, moved-from objects, 64-byte alignment, bounds-checked indices.
#include <algorithm>
#include <atomic>
#include <climits>
#include <cstdlib>
#include <new>
#include <random>
#include <thread>
#include <type_traits>
#include <unordered_map>
#include <unordered_set>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace tickers;

// ---------------------------------------------------------------- global allocation counter (test infrastructure)
namespace {
std::atomic<std::size_t> g_news{0};
}
void* operator new(std::size_t n) {
    g_news.fetch_add(1, std::memory_order_relaxed);
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

namespace {

using Rng = std::mt19937_64;
using Strings = std::vector<std::string>;

/// Number of operator new calls since construction.
struct AllocCount {
    std::size_t start = g_news.load();
    std::size_t get() const { return g_news.load() - start; }
};

Key k(std::string_view t) { return codec::pack(t); }

Strings random_tickers(Rng& g, std::size_t n, int max_len) {
    std::unordered_set<std::string> seen;
    Strings out;
    while (out.size() < n) {
        const int len = 1 + static_cast<int>(g() % static_cast<unsigned>(max_len));
        std::string s;
        for (int i = 0; i < len; ++i) s.push_back(static_cast<char>('A' + g() % 26));
        if (seen.insert(s).second) out.push_back(s);
    }
    return out;
}

Strings all_three_letters() {
    Strings out;
    for (char a = 'A'; a <= 'Z'; ++a)
        for (char b = 'A'; b <= 'Z'; ++b)
            for (char c = 'A'; c <= 'Z'; ++c) out.push_back({a, b, c});
    return out;
}

std::vector<Key> pack_all(const Strings& v) {
    std::vector<Key> out;
    for (const auto& s : v) out.push_back(k(s));
    return out;
}

std::vector<std::byte> wire(std::string_view s) {
    std::vector<std::byte> v;
    for (char c : s) v.push_back(static_cast<std::byte>(c));
    return v;
}

/// Every key hashes to the same value: the table must still be correct.
struct ConstHash {
    std::size_t operator()(std::string_view) const noexcept { return 42; }
};

}  // namespace

// ===================================================================================== Part 1: TickerMap

TEST(put_get_remove_basics, "part1") {
    TickerMap m;
    CHECK_EQ(m.size(), 0u);
    CHECK_EQ(m.get("AAPL"), std::nullopt);
    CHECK(!m.contains("AAPL"));
    CHECK_EQ(m.put("AAPL", 100), std::nullopt);
    CHECK_EQ(m.put("AAPL", 150), std::optional<long long>(100));  // returns the old value
    CHECK_EQ(m.get("AAPL"), std::optional<long long>(150));
    CHECK_EQ(m.size(), 1u);
    CHECK_EQ(m.remove("AAPL"), std::optional<long long>(150));
    CHECK_EQ(m.remove("AAPL"), std::nullopt);
    CHECK_EQ(m.size(), 0u);
    CHECK_EQ(m.get("AAPL"), std::nullopt);
}

TEST(zero_value_is_not_absent, "part1,edge") {
    TickerMap m;
    m.put("ZERO", 0);
    CHECK(m.contains("ZERO"));
    CHECK_EQ(m.get("ZERO"), std::optional<long long>(0));
    m.put("NEG", -5);
    CHECK_EQ(m.get("NEG"), std::optional<long long>(-5));
}

TEST(empty_string_is_an_ordinary_key, "part1,edge") {
    TickerMap m;
    m.put("", 7);
    CHECK_EQ(m.get(""), std::optional<long long>(7));
    CHECK_EQ(m.size(), 1u);
}

TEST(absurd_sizes_throw_length_error, "part1,edge,cpp") {
    // a size_t parameter turns "-1" into SIZE_MAX: refuse politely instead of overflowing or throwing bad_alloc
    CHECK_THROWS_AS(TickerMap(static_cast<std::size_t>(-1)), std::length_error);
    CHECK_THROWS_AS(LongTickerMap(static_cast<std::size_t>(-1)), std::length_error);
}

TEST(add_accumulates, "part1") {
    TickerMap m;
    CHECK_EQ(m.add("MSFT", 5), 5);
    CHECK_EQ(m.add("MSFT", 3), 8);
    CHECK_EQ(m.add("MSFT", -10), -2);
    CHECK_EQ(m.get("MSFT"), std::optional<long long>(-2));
    CHECK_EQ(m.size(), 1u);
}

TEST(add_overflow_leaves_the_table_untouched, "part1,edge") {
    TickerMap m;
    m.put("BIG", LLONG_MAX);
    CHECK_THROWS_AS(m.add("BIG", 1), std::overflow_error);
    CHECK_EQ(m.get("BIG"), std::optional<long long>(LLONG_MAX));
    m.put("LOW", LLONG_MIN);
    CHECK_THROWS_AS(m.add("LOW", -1), std::overflow_error);
    CHECK_EQ(m.get("LOW"), std::optional<long long>(LLONG_MIN));
    CHECK_EQ(m.add("NEWKEY", LLONG_MAX), LLONG_MAX);  // a new key starts from 0: no overflow
    CHECK_EQ(m.size(), 3u);
}

TEST(grows_past_many_resizes, "part1,edge") {
    TickerMap m;
    for (int i = 0; i < 100000; ++i) {
        m.put("K" + std::to_string(i), i);
        if ((m.size() + m.tombstones()) * 4 > m.capacity() * 3) CHECK(false, "load factor too high at " + std::to_string(i));
    }
    CHECK_EQ(m.size(), 100000u);
    for (int i = 0; i < 100000; ++i) CHECK_EQ(m.get("K" + std::to_string(i)), std::optional<long long>(i));
    CHECK_EQ(m.get("K100000"), std::nullopt);
}

TEST(expected_size_prevents_resizing, "part1,edge") {
    TickerMap m(10000);
    const std::size_t cap = m.capacity();
    for (int i = 0; i < 10000; ++i) m.put("S" + std::to_string(i), i);
    CHECK_EQ(m.capacity(), cap, "a presized map must not need to grow");
}

TEST(every_key_with_the_same_hash_still_works, "part1,edge") {
    BasicTickerMap<ConstHash> m;
    std::vector<std::string> keys;
    for (int mask = 0; mask < 1024; ++mask) {
        std::string s;
        for (int b = 0; b < 10; ++b) s += ((mask >> b) & 1) == 0 ? "Aa" : "BB";
        keys.push_back(s);
    }
    for (std::size_t i = 0; i < keys.size(); ++i) CHECK_EQ(m.put(keys[i], static_cast<long long>(i)), std::nullopt);
    for (std::size_t i = 0; i < keys.size(); ++i) CHECK_EQ(m.get(keys[i]), std::optional<long long>(i));
    for (std::size_t i = 0; i < keys.size(); i += 2) CHECK_EQ(m.remove(keys[i]), std::optional<long long>(i));
    for (std::size_t i = 0; i < keys.size(); ++i)
        CHECK_EQ(m.get(keys[i]), i % 2 == 0 ? std::nullopt : std::optional<long long>(i));
    CHECK_EQ(m.size(), 512u);
}

TEST(deleting_the_middle_of_a_probe_chain_does_not_hide_later_keys, "part1,edge") {
    BasicTickerMap<ConstHash> m;  // one long probe chain
    m.put("AaAa", 1);
    m.put("AaBB", 2);
    m.put("BBAa", 3);
    m.put("BBBB", 4);
    CHECK_EQ(m.remove("AaAa"), std::optional<long long>(1));  // chain head
    CHECK_EQ(m.get("AaBB"), std::optional<long long>(2));
    CHECK_EQ(m.get("BBAa"), std::optional<long long>(3));
    CHECK_EQ(m.get("BBBB"), std::optional<long long>(4));
    CHECK_EQ(m.remove("AaBB"), std::optional<long long>(2));  // chain middle
    CHECK_EQ(m.get("BBAa"), std::optional<long long>(3));
    CHECK_EQ(m.get("BBBB"), std::optional<long long>(4));
    m.put("AaAa", 10);  // re-insert: neither lost nor duplicated
    CHECK_EQ(m.size(), 3u);
    std::unordered_set<std::string> seen;
    m.for_each([&](std::string_view key, long long) { CHECK(seen.insert(std::string(key)).second, "duplicate key in for_each"); });
    CHECK(seen == (std::unordered_set<std::string>{"AaAa", "BBAa", "BBBB"}));
}

TEST(reinserting_a_deleted_key_reuses_the_tombstone, "part1,edge") {
    TickerMap m;
    for (int i = 0; i < 5; ++i) m.put("Q" + std::to_string(i), i);
    const std::size_t cap = m.capacity();
    for (int round = 0; round < 100000; ++round) {
        m.remove("Q3");
        m.put("Q3", round);
    }
    CHECK_EQ(m.capacity(), cap, "remove + put of the same key must not grow the table");
    CHECK_EQ(m.size(), 5u);
    CHECK_EQ(m.get("Q3"), std::optional<long long>(99999));
    CHECK_EQ(m.tombstones(), 0u, "re-using a tombstone must take it off the count");
}

TEST(tombstone_churn_does_not_bloat_the_table_or_loop_forever, "part1,edge") {
    // new tickers list and old ones delist: at most 10 live keys, 300k distinct keys overall
    TickerMap m;
    for (int i = 0; i < 300000; ++i) {
        m.put("N" + std::to_string(i), i);
        if (i >= 10) m.remove("N" + std::to_string(i - 10));
        if (m.get("never-there").has_value()) CHECK(false, "found a key that was never inserted");  // would spin without empty slots
    }
    CHECK_EQ(m.size(), 10u);
    CHECK_LE(m.capacity(), 1024u, "tombstones are never cleaned");
    CHECK_LE(m.tombstones() + m.size(), m.capacity() * 3 / 4);
}

TEST(random_operations_agree_with_std_unordered_map, "part1") {
    Rng g(0);
    TickerMap mine;
    std::unordered_map<std::string, long long> ref;
    const Strings universe = random_tickers(g, 600, 6);
    for (int step = 0; step < 200000; ++step) {
        const std::string& key = universe[g() % universe.size()];
        switch (g() % 5) {
            case 0: {
                const long long v = static_cast<long long>(g() % 1000) - 500;
                std::optional<long long> old;
                if (auto it = ref.find(key); it != ref.end()) old = it->second;
                ref[key] = v;
                CHECK_EQ(mine.put(key, v), old);
                break;
            }
            case 1: {
                const long long d = static_cast<long long>(g() % 100) - 50;
                CHECK_EQ(mine.add(key, d), ref[key] += d);
                break;
            }
            case 2: {
                std::optional<long long> old;
                if (auto it = ref.find(key); it != ref.end()) { old = it->second; ref.erase(it); }
                CHECK_EQ(mine.remove(key), old);
                break;
            }
            default: {
                auto it = ref.find(key);
                CHECK_EQ(mine.get(key), it == ref.end() ? std::nullopt : std::optional<long long>(it->second));
                CHECK_EQ(mine.contains(key), it != ref.end());
            }
        }
        CHECK_EQ(mine.size(), ref.size());
    }
    std::unordered_map<std::string, long long> copy;
    mine.for_each([&](std::string_view key, long long v) { copy[std::string(key)] = v; });
    CHECK(copy == ref);
}

TEST(probe_length_stays_short_on_realistic_tickers, "part1") {
    TickerMap m;  // AAA, AAB, AAC, ... : neighbours in the key space must not become neighbours in the table
    for (const auto& t : all_three_letters()) m.put(t, 1);
    CHECK_EQ(m.size(), 17576u);
    CHECK_LE(m.max_probe_length(), 64u);
}

TEST(lookups_by_string_view_allocate_nothing, "part1,cpp") {
    TickerMap m;
    const std::string long_key(40, 'X');  // longer than the small-string buffer: storing it allocates once
    m.put("AAPL", 1);
    m.put(long_key, 2);
    const AllocCount a;
    long long sum = 0;
    for (int i = 0; i < 1000; ++i) {
        sum += m.get("AAPL").value();
        sum += m.get(std::string_view(long_key)).value();  // a std::string_view parameter: no temporary std::string
        sum += m.contains("MSFT") ? 1 : 0;
        sum += m.add("AAPL", 1);
    }
    CHECK_EQ(a.get(), 0u);
    CHECK_GT(sum, 0);
}

TEST(short_keys_live_inside_the_slots_so_inserting_allocates_nothing, "part1,cpp") {
    Rng g(1);
    const Strings tickers = random_tickers(g, 5000, 8);  // <= 8 chars: inside std::string's small buffer
    TickerMap m(5000);                                   // presized: no rehash either
    const AllocCount a;
    for (const auto& t : tickers) m.put(t, 1);
    CHECK_EQ(a.get(), 0u);
    CHECK_EQ(m.size(), 5000u);
}

TEST(an_embedded_nul_makes_a_different_key, "part1,cpp") {
    TickerMap m;
    m.put(std::string_view("AB\0CD", 5), 1);  // 5 bytes
    m.put("AB", 2);                           // 2 bytes: a C string stops at the NUL, a string_view with a length does not
    CHECK_EQ(m.size(), 2u);
    CHECK_EQ(m.get(std::string_view("AB\0CD", 5)), std::optional<long long>(1));
    CHECK_EQ(m.get("AB"), std::optional<long long>(2));
}

TEST(a_million_operations_under_two_seconds, "part1,perf") {
    Rng g(0);
    const Strings tickers = random_tickers(g, 200000, 8);
    CHECK_WITHIN_MS(2000, TickerMap m; for (int i = 0; i < 1'000'000; ++i) m.add(tickers[g() % tickers.size()], 1); long long total = 0;
                    for (const auto& t : tickers) total += m.get(t).value_or(0); CHECK_EQ(total, 1'000'000););
}

// ===================================================================================== Part 2: codec

TEST(documented_encoding, "part2") {
    const Key expected = (1ull << 35) | (1ull << 30) | (16ull << 25) | (12ull << 20);  // A A P L
    CHECK_EQ(codec::pack("AAPL"), expected);
    CHECK_EQ(codec::pack("A"), 1ull << 35);
    CHECK_EQ(codec::pack("ZZZZZZZZ"), (26ull << 35) | (26ull << 30) | (26ull << 25) | (26ull << 20) | (26ull << 15) | (26ull << 10) | (26ull << 5) | 26ull);
    CHECK(codec::parse("AAPL") == codec::Parsed(codec::Ticker{expected}));
}

TEST(round_trip, "part2") {
    for (const char* t : {"A", "AB", "IBM", "AAPL", "GOOGL", "BRKBXX", "ABCDEFG", "ABCDEFGH"}) CHECK_EQ(codec::unpack(codec::pack(t)), std::string(t));
    Rng g(0);
    for (const auto& t : random_tickers(g, 20000, 8)) CHECK_EQ(codec::unpack(codec::pack(t)), t);
}

TEST(distinct_tickers_get_distinct_positive_keys, "part2") {
    std::unordered_set<Key> seen;
    for (const auto& t : all_three_letters()) {
        const Key key = k(t);
        CHECK(key > 0 && key < (1ull << 40));
        CHECK(seen.insert(key).second, "collision at " + t);
    }
    CHECK(k("A") != k("AA") && k("AA") != k("AAA") && k("A") != k("AAA"));  // prefixes are different tickers
}

TEST(invalid_tickers, "part2,edge") {
    const std::vector<std::string_view> bad = {"", "ABCDEFGHI", "aapl", "AaPL", "BRK.B", "BRK-B", "A1", "A B", " AAPL", "AAPL ",
                                               "\xC3\x89",          // "É" in UTF-8: bytes >= 0x80
                                               "\xEF\xBC\xA1\xEF\xBC\xA2"};  // fullwidth "AB" in UTF-8
    for (std::string_view s : bad) {
        const codec::Parsed p = codec::parse(s);
        const auto* inv = std::get_if<codec::Invalid>(&p);
        REQUIRE(inv != nullptr, "should be invalid: " + std::string(s));
        CHECK(std::string(codec::what(inv->error)).size() > 3);
        CHECK_THROWS_AS(codec::pack(s), std::invalid_argument);
    }
}

TEST(the_invalid_result_says_what_and_where, "part2,edge") {
    CHECK(std::get<codec::Invalid>(codec::parse("")).error == codec::Error::Empty);
    CHECK(std::get<codec::Invalid>(codec::parse("ABCDEFGHI")).error == codec::Error::TooLong);
    const auto bad = std::get<codec::Invalid>(codec::parse("AB.C"));
    CHECK(bad.error == codec::Error::BadChar);
    CHECK_EQ(bad.position, 2u);
}

TEST(embedded_nul_is_invalid_not_truncated, "part2,edge,cpp") {
    CHECK(std::holds_alternative<codec::Invalid>(codec::parse(std::string_view("AB\0CD", 5))));  // 5 bytes, one is NUL
    CHECK_EQ(codec::pack(std::string_view("AB\0CD")), codec::pack("AB"));                         // a string literal -> length 2
}

TEST(char_signedness_does_not_leak_into_validation, "part2,edge,cpp") {
    for (int c = 128; c < 256; ++c) {
        const std::string s{'A', static_cast<char>(c)};
        CHECK(std::holds_alternative<codec::Invalid>(codec::parse(s)), "byte " + std::to_string(c));
    }
}

TEST(invalid_keys_cannot_be_unpacked, "part2,edge") {
    const Key bad[] = {0, ~0ull, 1ull << 40, 0x7FFFFFFFFFFFFFFFull,
                       (1ull << 35) | (1ull << 25),  // A, empty, A: a letter after a 0 field
                       27ull << 35,                  // field 27 is not a letter
                       31ull << 35, 1ull};           // the last field set with everything before it empty
    for (Key key : bad) {
        CHECK(!codec::is_valid_key(key), "is_valid_key(" + std::to_string(key) + ")");
        CHECK_THROWS_AS(codec::unpack(key), std::invalid_argument);
    }
    CHECK(codec::is_valid_key(k("QQQ")));
}

TEST(wire_format_matches_string_packing, "part2") {
    CHECK_EQ(codec::pack_wire(wire("AAPL    "), 0), k("AAPL"));
    CHECK_EQ(codec::pack_wire(wire("A       "), 0), k("A"));
    CHECK_EQ(codec::pack_wire(wire("ABCDEFGH"), 0), k("ABCDEFGH"));
    const auto msg = wire("xx12AAPL    yy");  // inside a bigger message
    CHECK_EQ(codec::pack_wire(msg, 4), k("AAPL"));
    Rng g(1);
    for (const auto& t : random_tickers(g, 5000, 8)) CHECK_EQ(codec::pack_wire(wire((t + "        ").substr(0, 8)), 0), k(t));
}

TEST(malformed_wire_fields, "part2,edge") {
    const std::vector<std::string_view> bad = {"        ", " AAPL   ", "AA PL   ", "aapl    ", std::string_view("AAPL\0\0\0\0", 8),
                                               "AAP1    ", "AAPL.B  ", "AAP\xC3\x89    "};
    for (std::string_view s : bad) {
        const auto w = wire(s);
        CHECK_THROWS_AS(codec::pack_wire(w, 0), std::invalid_argument, std::string(s));
    }
}

TEST(wire_field_must_fit_in_the_buffer, "part2,edge") {
    CHECK_THROWS_AS(codec::pack_wire(wire("AAPL"), 0), std::out_of_range);
    CHECK_THROWS_AS(codec::pack_wire(wire("AAPL    "), 1), std::out_of_range);
    CHECK_THROWS_AS(codec::pack_wire(wire(""), 0), std::out_of_range);
}

TEST(a_huge_offset_must_not_wrap_around, "part2,edge,cpp") {
    const auto w = wire("AAPL    ");
    // `off + 8 > size` is false for off = SIZE_MAX - 3 (the sum wraps to 4) and the read would go far out of bounds
    CHECK_THROWS_AS(codec::pack_wire(w, static_cast<std::size_t>(-1) - 3), std::out_of_range);
    CHECK_THROWS_AS(codec::pack_wire(w, static_cast<std::size_t>(-1)), std::out_of_range);
}

// ---- LongTickerMap

TEST(long_map_basics, "part2") {
    LongTickerMap m;
    CHECK_EQ(m.get(k("AAPL"), -1), -1);
    CHECK(!m.contains(k("AAPL")));
    CHECK(m.put(k("AAPL"), 10));
    CHECK(!m.put(k("AAPL"), 20));
    CHECK_EQ(m.get(k("AAPL"), -1), 20);
    CHECK_EQ(m.add(k("AAPL"), 5), 25);
    CHECK_EQ(m.add(k("MSFT"), 7), 7);  // a new key starts from 0
    CHECK_EQ(m.size(), 2u);
    CHECK(m.remove(k("AAPL")));
    CHECK(!m.remove(k("AAPL")));
    CHECK_EQ(m.size(), 1u);
    CHECK_EQ(m.get(k("AAPL"), 0), 0);
}

TEST(long_map_rejects_the_two_marker_keys, "part2,edge") {
    LongTickerMap m;
    for (Key bad : {Key{0}, TOMB}) {
        CHECK_THROWS_AS(m.put(bad, 1), std::invalid_argument);
        CHECK_THROWS_AS(m.get(bad, 0), std::invalid_argument);
        CHECK_THROWS_AS(m.add(bad, 1), std::invalid_argument);
        CHECK_THROWS_AS(m.remove(bad), std::invalid_argument);
        CHECK_THROWS_AS(m.contains(bad), std::invalid_argument);
    }
    CHECK(m.put(TOMB - 1, 1));
    CHECK_EQ(m.get(TOMB - 1, 0), 1);
    CHECK(m.put(1ull << 63, 5));  // large keys are fine
}

TEST(minus_one_converted_to_a_key_is_the_tombstone_marker, "part2,edge,cpp") {
    LongTickerMap m;
    const int signed_minus_one = -1;
    CHECK_THROWS_AS(m.put(static_cast<Key>(signed_minus_one), 1), std::invalid_argument);  // -1 converts to 0xFFFF...FFFF
}

TEST(zero_and_negative_values_are_real_values, "part2,edge") {
    LongTickerMap m;
    m.put(k("Z"), 0);
    CHECK(m.contains(k("Z")));
    CHECK_EQ(m.get(k("Z"), 99), 0);
    m.put(k("N"), LLONG_MIN);
    CHECK_EQ(m.get(k("N"), 0), LLONG_MIN);
}

TEST(long_map_add_overflow_leaves_the_value_alone, "part2,edge") {
    LongTickerMap m;
    m.put(k("BIG"), LLONG_MAX);
    CHECK_THROWS_AS(m.add(k("BIG"), 1), std::overflow_error);
    CHECK_EQ(m.get(k("BIG"), 0), LLONG_MAX);
    CHECK_EQ(m.size(), 1u);
}

TEST(long_map_grows_and_keeps_everything, "part2,edge") {
    LongTickerMap m;
    Rng g(3);
    const Strings tickers = random_tickers(g, 100000, 8);
    for (std::size_t i = 0; i < tickers.size(); ++i) {
        m.put(k(tickers[i]), static_cast<long long>(i));
        if ((m.size() + m.tombstones()) * 4 > m.capacity() * 3) CHECK(false, "load factor too high");
    }
    CHECK_EQ(m.size(), tickers.size());
    for (std::size_t i = 0; i < tickers.size(); ++i) CHECK_EQ(m.get(k(tickers[i]), -1), static_cast<long long>(i));
}

TEST(long_map_tombstone_churn_stays_bounded, "part2,edge") {
    LongTickerMap m;
    for (Key i = 1; i <= 400000; ++i) {
        m.put(i, static_cast<long long>(i));
        if (i > 10) CHECK(m.remove(i - 10));
        if (m.get(TOMB - 1, -5) != -5) CHECK(false, "found a key that was never inserted");  // would spin without empty slots
    }
    CHECK_EQ(m.size(), 10u);
    CHECK_LE(m.capacity(), 1024u);
}

TEST(long_map_reuses_tombstones_and_counts_them_correctly, "part2,edge") {
    LongTickerMap m;
    for (Key key = 100; key < 105; ++key) m.put(key, 1);
    const std::size_t cap = m.capacity();
    CHECK(m.remove(103));
    CHECK_EQ(m.tombstones(), 1u);
    CHECK(m.put(103, 7));
    CHECK_EQ(m.tombstones(), 0u);
    for (int round = 0; round < 50000; ++round) {
        m.remove(103);
        m.put(103, round);
    }
    CHECK_EQ(m.capacity(), cap);
    CHECK_EQ(m.size(), 5u);
    CHECK_EQ(m.tombstones(), 0u);
}

TEST(long_map_deleting_in_the_middle_of_a_chain_keeps_the_rest, "part2,edge") {
    LongTickerMap m(4);
    Rng g(4);
    const Strings tickers = random_tickers(g, 3000, 3);
    for (const auto& t : tickers) m.put(k(t), 1);
    for (std::size_t i = 0; i < tickers.size(); i += 2) CHECK(m.remove(k(tickers[i])));
    for (std::size_t i = 0; i < tickers.size(); ++i) CHECK_EQ(m.get(k(tickers[i]), -1), i % 2 == 0 ? -1 : 1, tickers[i]);
}

TEST(long_map_random_operations_agree_with_std_unordered_map, "part2") {
    Rng g(0);
    LongTickerMap mine;
    std::unordered_map<Key, long long> ref;
    const auto universe = pack_all(random_tickers(g, 800, 8));
    for (int step = 0; step < 300000; ++step) {
        const Key key = universe[g() % universe.size()];
        switch (g() % 5) {
            case 0: {
                const long long v = static_cast<long long>(g() % 1000) - 500;
                const bool fresh = ref.find(key) == ref.end();
                ref[key] = v;
                CHECK_EQ(mine.put(key, v), fresh);
                break;
            }
            case 1: {
                const long long d = static_cast<long long>(g() % 100) - 50;
                CHECK_EQ(mine.add(key, d), ref[key] += d);
                break;
            }
            case 2: CHECK_EQ(mine.remove(key), ref.erase(key) == 1); break;
            default: {
                auto it = ref.find(key);
                CHECK_EQ(mine.get(key, -777), it == ref.end() ? -777 : it->second);
                CHECK_EQ(mine.contains(key), it != ref.end());
            }
        }
        CHECK_EQ(mine.size(), ref.size());
    }
    std::unordered_map<Key, long long> copy;
    mine.for_each([&](Key key, long long v) { copy[key] = v; });
    CHECK(copy == ref);
}

TEST(the_hash_spreads_packed_keys_whose_low_bits_are_zero, "part2,edge") {
    // a short packed ticker has all-zero low bits: `key & mask` would put them all in one slot
    LongTickerMap m;
    for (const auto& t : all_three_letters()) m.put(k(t), 1);
    CHECK_EQ(m.size(), 17576u);
    CHECK_LE(m.max_probe_length(), 64u);
    Rng g(5);
    LongTickerMap m2;
    for (const auto& t : random_tickers(g, 8000, 8)) m2.put(k(t), 1);
    CHECK_LE(m2.max_probe_length(), 64u);
}

TEST(long_map_agrees_with_ticker_map_on_the_same_feed, "part2") {
    Rng g(6);
    const Strings tickers = random_tickers(g, 3000, 8);
    TickerMap str_map;
    LongTickerMap long_map;
    for (int i = 0; i < 200000; ++i) {
        const std::string& t = tickers[g() % tickers.size()];
        const long long q = 1 + static_cast<long long>(g() % 500);
        CHECK_EQ(str_map.add(t, q), long_map.add(k(t), q));
    }
    str_map.for_each([&](std::string_view t, long long v) { CHECK_EQ(long_map.get(k(t), -1), v); });
    CHECK_EQ(str_map.size(), long_map.size());
}

TEST(steady_state_adds_do_not_allocate, "part2,cpp") {
    Rng g(0);
    const auto keys = pack_all(random_tickers(g, 8000, 8));
    LongTickerMap m(keys.size());
    for (Key key : keys) m.put(key, 0);
    std::vector<std::uint32_t> picks(1'600'000);
    for (auto& p : picks) p = static_cast<std::uint32_t>(g() % keys.size());
    const AllocCount a;
    for (std::uint32_t p : picks) m.add(keys[p], 1);
    CHECK_EQ(a.get(), 0u);
}

TEST(a_flat_table_allocates_once_a_node_based_map_once_per_entry, "part2,cpp") {
    Rng g(0);
    const auto keys = pack_all(random_tickers(g, 8000, 8));
    {
        const AllocCount a;
        LongTickerMap m(keys.size());
        for (Key key : keys) m.put(key, 1);
        CHECK_EQ(a.get(), 1u);  // the slot array
    }
    {
        const AllocCount a;
        std::unordered_map<Key, long long> m;
        m.reserve(keys.size());
        for (Key key : keys) m[key] = 1;
        CHECK_GE(a.get(), keys.size());  // one heap node per entry
    }
}

TEST(five_million_adds_on_eight_thousand_tickers_under_two_seconds, "part2,perf") {
    Rng g(0);
    const auto keys = pack_all(random_tickers(g, 8000, 8));
    CHECK_WITHIN_MS(2000, LongTickerMap m; for (int i = 0; i < 5'000'000; ++i) m.add(keys[g() % keys.size()], 1); long long total = 0;
                    for (Key key : keys) total += m.get(key, 0); CHECK_EQ(total, 5'000'000););
}

// ===================================================================================== Part 3: perfect hash

namespace {
void check_minimal_perfect(const std::vector<Key>& universe, const SymbolIndex& idx) {
    const std::size_t n = universe.size();
    CHECK_EQ(idx.size(), n);
    std::vector<std::uint8_t> hit(n, 0);
    for (Key key : universe) {
        const int i = idx.index_of(key);
        if (i < 0 || static_cast<std::size_t>(i) >= n) { CHECK(false, "index out of range for " + std::to_string(key)); continue; }
        CHECK(!hit[static_cast<std::size_t>(i)], "two keys share index " + std::to_string(i));
        hit[static_cast<std::size_t>(i)] = 1;
        CHECK_EQ(idx.key_at(static_cast<std::size_t>(i)), key);
    }
}
}  // namespace

TEST(small_universe, "part3") {
    const auto u = pack_all({"AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META"});
    const SymbolIndex idx = SymbolIndex::build(u);
    check_minimal_perfect(u, idx);
    CHECK_EQ(idx.index_of(k("IBM")), -1);
}

TEST(degenerate_universes, "part3,edge") {
    const SymbolIndex empty = SymbolIndex::build({});
    CHECK_EQ(empty.size(), 0u);
    CHECK_EQ(empty.index_of(k("A")), -1);
    const std::vector<Key> one{k("X")};
    const SymbolIndex single = SymbolIndex::build(one);
    CHECK_EQ(single.index_of(k("X")), 0);
    CHECK_EQ(single.index_of(k("Y")), -1);
    const auto two = pack_all({"A", "B"});
    check_minimal_perfect(two, SymbolIndex::build(two));
    for (int n = 1; n <= 40; ++n) {
        Rng g(static_cast<unsigned>(n));
        const auto u = pack_all(random_tickers(g, static_cast<std::size_t>(n), 6));
        check_minimal_perfect(u, SymbolIndex::build(u));
    }
}

TEST(rejects_bad_universes, "part3,edge") {
    const Key a = k("A");
    const std::vector<Key> dup{a, a}, zero{a, 0}, tomb{a, TOMB};
    CHECK_THROWS_AS(SymbolIndex::build(dup), std::invalid_argument);
    CHECK_THROWS_AS(SymbolIndex::build(zero), std::invalid_argument);
    CHECK_THROWS_AS(SymbolIndex::build(tomb), std::invalid_argument);
}

TEST(keys_outside_the_universe_are_recognised, "part3") {
    Rng g(7);
    const Strings inside = random_tickers(g, 8000, 6);
    const std::unordered_set<std::string> all(inside.begin(), inside.end());
    const auto u = pack_all(inside);
    const SymbolIndex idx = SymbolIndex::build(u);
    int tested = 0;
    for (const auto& t : random_tickers(g, 60000, 8)) {
        if (all.count(t)) continue;
        CHECK_EQ(idx.index_of(k(t)), -1, t);
        ++tested;
    }
    CHECK_GT(tested, 50000);
    for (Key odd : {Key{0}, TOMB, Key{1}, 1ull << 63}) CHECK_EQ(idx.index_of(odd), -1);
}

TEST(dense_structured_universe, "part3,edge") {
    const auto u = pack_all(all_three_letters());  // AAA..ZZZ: the low 25 bits of every key are 0
    check_minimal_perfect(u, SymbolIndex::build(u));
}

TEST(build_order_does_not_matter, "part3,edge") {
    Rng g(8);
    Strings tickers = random_tickers(g, 5000, 8);
    const auto u = pack_all(tickers);
    std::shuffle(tickers.begin(), tickers.end(), g);
    const auto shuffled = pack_all(tickers);
    check_minimal_perfect(u, SymbolIndex::build(u));
    check_minimal_perfect(shuffled, SymbolIndex::build(shuffled));
}

TEST(builds_one_hundred_thousand_symbols_quickly, "part3,perf") {
    Rng g(0);
    const auto u = pack_all(random_tickers(g, 100000, 8));
    CHECK_WITHIN_MS(2000, check_minimal_perfect(u, SymbolIndex::build(u)););
}

TEST(twenty_million_lookups, "part3,perf") {
    Rng g(0);
    const auto u = pack_all(random_tickers(g, 8000, 8));
    const SymbolIndex idx = SymbolIndex::build(u);
    std::vector<std::uint32_t> picks(1 << 16);
    for (auto& p : picks) p = static_cast<std::uint32_t>(g() % u.size());
    CHECK_WITHIN_MS(2000, long long sum = 0; for (int i = 0; i < 20'000'000; ++i) sum += idx.index_of(u[picks[static_cast<std::size_t>(i) & (picks.size() - 1)]]);
                    CHECK_GT(sum, 0););
}

// ---- FrozenTickerMap

TEST(frozen_basics, "part3") {
    FrozenTickerMap m(Strings{"AAPL", "MSFT", "GOOG"});
    CHECK_EQ(m.size(), 3u);
    CHECK(m.contains(k("AAPL")));
    CHECK(!m.contains(k("IBM")));
    CHECK_EQ(m.get(k("AAPL"), -1), 0);  // in the universe, never written: 0 and not absent
    CHECK_EQ(m.get(k("IBM"), -1), -1);
    CHECK_EQ(m.add(k("AAPL"), 100), 100);
    CHECK_EQ(m.add(k("AAPL"), 30), 130);
    CHECK(m.put(k("MSFT"), 5));
    CHECK(!m.put(k("IBM"), 5));
    CHECK_EQ(m.get(k("MSFT"), -1), 5);
    CHECK_THROWS_AS(m.add(k("IBM"), 1), std::invalid_argument);
}

TEST(frozen_rejects_bad_universes, "part3,edge") {
    const Strings dup{"AAPL", "AAPL"}, lower{"AAPL", "brk.b"}, blank{""};
    CHECK_THROWS_AS(FrozenTickerMap(dup), std::invalid_argument);
    CHECK_THROWS_AS(FrozenTickerMap(lower), std::invalid_argument);
    CHECK_THROWS_AS(FrozenTickerMap(blank), std::invalid_argument);
    const FrozenTickerMap empty{Strings{}};
    CHECK_EQ(empty.size(), 0u);
    CHECK_EQ(empty.get(k("A"), -3), -3);
    CHECK_EQ(empty.index_of(k("A")), -1);
}

TEST(frozen_marker_keys_are_just_absent, "part3,edge") {
    FrozenTickerMap m(Strings{"A"});
    for (Key bad : {Key{0}, TOMB}) {
        CHECK_EQ(m.index_of(bad), -1);
        CHECK(!m.contains(bad));
        CHECK_EQ(m.get(bad, 42), 42);
        CHECK(!m.put(bad, 1));
    }
}

TEST(frozen_overflow_throws_and_keeps_the_value, "part3,edge") {
    FrozenTickerMap m(Strings{"A"});
    m.put(k("A"), LLONG_MAX);
    CHECK_THROWS_AS(m.add(k("A"), 1), std::overflow_error);
    CHECK_EQ(m.get(k("A"), 0), LLONG_MAX);
    const int i = m.index_of(k("A"));
    CHECK_THROWS_AS(m.add_at(i, 1), std::overflow_error);
    CHECK_EQ(m.get_at(i), LLONG_MAX);
}

TEST(index_based_fast_path, "part3") {
    Rng g(1);
    const Strings universe = random_tickers(g, 2000, 8);
    FrozenTickerMap m(universe);
    for (const auto& t : universe) {
        const int i = m.index_of(k(t));
        CHECK(i >= 0 && static_cast<std::size_t>(i) < universe.size());
        CHECK_EQ(m.key_at(i), k(t));
        m.add_at(i, 3);
    }
    for (const auto& t : universe) CHECK_EQ(m.get(k(t), -1), 3);
}

TEST(indices_are_bounds_checked, "part3,edge,cpp") {
    FrozenTickerMap m(Strings{"A", "B"});
    CHECK_THROWS_AS(m.add_at(-1, 1), std::out_of_range);  // not undefined behaviour
    CHECK_THROWS_AS(m.add_at(2, 1), std::out_of_range);
    CHECK_THROWS_AS(m.get_at(2), std::out_of_range);
    CHECK_THROWS_AS(m.key_at(-1), std::out_of_range);
    CHECK_THROWS_AS(m.key_at(2), std::out_of_range);
}

TEST(frozen_agrees_with_the_long_map_on_the_same_feed, "part3") {
    Rng g(2);
    const Strings universe = random_tickers(g, 8000, 8);
    FrozenTickerMap frozen(universe);
    LongTickerMap open;
    std::unordered_map<Key, long long> ref;
    const auto keys = pack_all(universe);
    for (int i = 0; i < 300000; ++i) {
        const Key key = keys[g() % keys.size()];
        const long long q = static_cast<long long>(g() % 1000);
        CHECK_EQ(open.add(key, q), frozen.add(key, q));
        ref[key] += q;
    }
    for (Key key : keys) CHECK_EQ(frozen.get(key, -1), ref.count(key) ? ref[key] : 0);
}

TEST(twenty_million_indexed_updates_under_two_seconds, "part3,perf") {
    Rng g(0);
    const Strings universe = random_tickers(g, 8000, 8);
    FrozenTickerMap m(universe);
    const auto keys = pack_all(universe);
    std::vector<std::uint32_t> picks(1 << 16);
    for (auto& p : picks) p = static_cast<std::uint32_t>(g() % keys.size());
    CHECK_WITHIN_MS(2000, for (int i = 0; i < 20'000'000; ++i) m.add(keys[picks[static_cast<std::size_t>(i) & (picks.size() - 1)]], 1); long long total = 0;
                    for (Key key : keys) total += m.get(key, 0); CHECK_EQ(total, 20'000'000););
}

TEST(the_hot_path_does_not_allocate, "part3,cpp") {
    Rng g(0);
    const Strings universe = random_tickers(g, 8000, 8);
    FrozenTickerMap m(universe);
    const auto keys = pack_all(universe);
    std::vector<int> cached;
    for (Key key : keys) cached.push_back(m.index_of(key));
    const AllocCount a;
    for (int round = 0; round < 100; ++round) {
        for (Key key : keys) m.add(key, 1);
        for (int idx : cached) m.add_at(idx, 1);
    }
    CHECK_EQ(a.get(), 0u);
}

// ===================================================================================== Part 4: FixedTickerMap

TEST(fixed_basics, "part4") {
    FixedTickerMap m(100);
    CHECK_EQ(m.size(), 0u);
    CHECK_EQ(m.get(k("AAPL"), -1), -1);
    CHECK(!m.contains(k("AAPL")));
    CHECK(m.put(k("AAPL"), 10));
    CHECK(!m.put(k("AAPL"), 20));
    CHECK_EQ(m.get(k("AAPL"), -1), 20);
    CHECK_EQ(m.add(k("AAPL"), 5), 25);
    CHECK_EQ(m.add(k("MSFT"), 3), 3);
    CHECK_EQ(m.size(), 2u);
    CHECK(m.contains(k("MSFT")));
}

TEST(capacity_is_a_power_of_two_with_headroom, "part4,edge") {
    for (std::size_t n : {1u, 2u, 3u, 7u, 8u, 100u, 1000u, 4096u, 5000u}) {
        FixedTickerMap m(n);
        CHECK_EQ(m.max_entries(), n);
        CHECK(std::has_single_bit(m.capacity()), "capacity " + std::to_string(m.capacity()));
        CHECK_GE(m.capacity(), 2 * n);
    }
    CHECK_THROWS_AS(FixedTickerMap(0), std::invalid_argument);
    CHECK_THROWS_AS(FixedTickerMap((std::size_t{1} << 28) + 1), std::invalid_argument);
    CHECK_THROWS_AS(FixedTickerMap(static_cast<std::size_t>(-1)), std::invalid_argument);
}

TEST(a_full_table_rejects_new_keys_but_serves_old_ones, "part4,edge") {
    FixedTickerMap m(3);
    m.put(k("A"), 1);
    m.put(k("B"), 2);
    m.add(k("C"), 3);
    CHECK_THROWS_AS(m.put(k("D"), 4), std::length_error);
    CHECK_THROWS_AS(m.add(k("D"), 4), std::length_error);
    CHECK_EQ(m.size(), 3u);
    CHECK_EQ(m.get(k("D"), -1), -1);
    CHECK_EQ(m.add(k("B"), 3), 5);  // existing keys can still be updated
    CHECK(!m.put(k("C"), 9));
    CHECK_EQ(m.get(k("C"), -1), 9);
}

TEST(fixed_invalid_keys_and_overflow, "part4,edge") {
    FixedTickerMap m(10);
    for (Key bad : {Key{0}, TOMB}) {
        CHECK_THROWS_AS(m.put(bad, 1), std::invalid_argument);
        CHECK_THROWS_AS(m.get(bad, 0), std::invalid_argument);
        CHECK_THROWS_AS(m.add(bad, 1), std::invalid_argument);
        CHECK_THROWS_AS(m.contains(bad), std::invalid_argument);
    }
    m.put(k("BIG"), LLONG_MAX);
    CHECK_THROWS_AS(m.add(k("BIG"), 1), std::overflow_error);
    CHECK_EQ(m.get(k("BIG"), 0), LLONG_MAX);
}

TEST(access_after_close_fails_and_close_is_idempotent, "part4,edge") {
    FixedTickerMap m(10);
    m.put(k("A"), 1);
    m.close();
    m.close();
    CHECK_THROWS_AS(m.get(k("A"), 0), std::logic_error);
    CHECK_THROWS_AS(m.put(k("B"), 1), std::logic_error);
    CHECK_THROWS_AS(m.add(k("A"), 1), std::logic_error);
    CHECK_EQ(m.size(), 0u);
}

TEST(fixed_random_operations_agree_with_std_unordered_map, "part4") {
    Rng g(0);
    const auto keys = pack_all(random_tickers(g, 1000, 8));
    std::unordered_map<Key, long long> ref;
    FixedTickerMap m(1000);
    for (int step = 0; step < 300000; ++step) {
        const Key key = keys[g() % keys.size()];
        if (g() % 3 == 0) {
            const long long v = static_cast<long long>(g() % 1000);
            const bool fresh = ref.find(key) == ref.end();
            ref[key] = v;
            CHECK_EQ(m.put(key, v), fresh);
        } else {
            const long long d = static_cast<long long>(g() % 100);
            CHECK_EQ(m.add(key, d), ref[key] += d);
        }
        CHECK_EQ(m.size(), ref.size());
    }
    for (Key key : keys) CHECK_EQ(m.get(key, -1), ref.count(key) ? ref[key] : -1);
}

TEST(the_storage_is_cache_line_aligned, "part4,cpp") {
    for (std::size_t n : {1u, 100u, 5000u}) {
        FixedTickerMap m(n);
        CHECK_EQ(reinterpret_cast<std::uintptr_t>(m.data()) % 64, 0u);
    }
}

TEST(move_only_and_a_moved_from_map_is_empty_and_safe, "part4,cpp") {
    static_assert(!std::is_copy_constructible_v<FixedTickerMap>);
    static_assert(!std::is_copy_assignable_v<FixedTickerMap>);
    static_assert(std::is_nothrow_move_constructible_v<FixedTickerMap>);
    FixedTickerMap a(10);
    a.put(k("A"), 1);
    FixedTickerMap b = std::move(a);
    CHECK_EQ(b.get(k("A"), -1), 1);
    CHECK_EQ(a.size(), 0u);  // the compiler-generated move would have copied size_ and left a stale 1 behind
    CHECK_EQ(a.capacity(), 0u);
    CHECK_THROWS_AS(a.get(k("A"), 0), std::logic_error);
    FixedTickerMap c(4);
    c.put(k("Z"), 9);
    c = std::move(b);
    CHECK_EQ(c.get(k("A"), -1), 1);
    CHECK_EQ(c.get(k("Z"), -1), -1);  // c's old storage is gone
    CHECK_THROWS_AS(b.put(k("B"), 1), std::logic_error);
}

TEST(usable_from_another_thread, "part4,conc") {
    FixedTickerMap m(10);
    std::jthread t([&] { m.add(k("X"), 1); });  // no thread affinity: the join below orders the accesses
    t.join();
    CHECK_EQ(m.get(k("X"), 0), 1);
}

TEST(five_million_adds_and_no_allocation, "part4,perf") {
    Rng g(0);
    const auto keys = pack_all(random_tickers(g, 8000, 8));
    std::vector<std::uint32_t> picks(5'000'000);
    for (auto& p : picks) p = static_cast<std::uint32_t>(g() % keys.size());
    FixedTickerMap m(8000);
    for (Key key : keys) m.put(key, 0);
    const AllocCount a;
    CHECK_WITHIN_MS(2000, for (std::uint32_t p : picks) m.add(keys[p], 1););
    CHECK_EQ(a.get(), 0u);
    long long total = 0;
    for (Key key : keys) total += m.get(key, 0);
    CHECK_EQ(total, 5'000'000);
}

MT_MAIN()
