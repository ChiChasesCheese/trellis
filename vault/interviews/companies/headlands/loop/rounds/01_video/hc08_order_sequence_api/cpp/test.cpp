// hc08 · Order sequence API — C++20 tests.  Same cases as test/OrderSequenceTest.java plus C++-only edge cases (tag "cpp"):
// moved-from / copied objects, operator[] inserting on lookup, strict from_chars parsing, failed puts leaving no trace,
// int-range index arguments, unordered_map bucket memory, hash behaviour with strided ids.
#include <bit>
#include <climits>
#include <deque>
#include <iostream>
#include <random>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace oseq;

namespace oseq {
std::ostream& operator<<(std::ostream& os, const Entry& e) { return os << "Entry(" << e.id << "," << e.qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Put& p) { return os << "Put(" << p.id << "," << p.qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Delete& p) { return os << "Delete(" << p.id << "," << p.qty << ")"; }
std::ostream& operator<<(std::ostream& os, const CountUpTo& p) { return os << "CountUpTo(" << p.id << ")"; }
std::ostream& operator<<(std::ostream& os, const QtyUpTo& p) { return os << "QtyUpTo(" << p.id << ")"; }
std::ostream& operator<<(std::ostream& os, const IdAt& p) { return os << "IdAt(" << p.k << ")"; }
}  // namespace oseq

namespace {

using Lines = std::vector<std::string>;
using Entries = std::vector<Entry>;

Lines lines(const std::string& block) {
    Lines out;
    std::size_t pos = 0;
    while (pos < block.size()) {
        std::size_t nl = block.find('\n', pos);
        if (nl == std::string::npos) nl = block.size();
        out.push_back(block.substr(pos, nl - pos));
        pos = nl + 1;
    }
    return out;
}

/// Naive model (the Part 1 reference approach): a vector scanned linearly; used as the ground truth for differential tests.
struct Model {
    std::vector<std::pair<long long, long long>> list;  // {id, qty}
    int find(long long id) const {
        for (std::size_t i = 0; i < list.size(); ++i)
            if (list[i].first == id) return static_cast<int>(i);
        return -1;
    }
    void put(long long id, long long qty) { list.emplace_back(id, qty); }
    long long remove(long long id, long long qty) {
        const auto i = static_cast<std::size_t>(find(id));
        const long long left = list[i].second - qty;
        if (left == 0) list.erase(list.begin() + static_cast<std::ptrdiff_t>(i));
        else list[i].second = left;
        return left;
    }
    long long count(long long id) const { return find(id) + 1; }
    long long qty(long long id) const {
        long long s = 0;
        const int at = find(id);
        for (int i = 0; i <= at; ++i) s += list[static_cast<std::size_t>(i)].second;
        return s;
    }
    long long id_at(int k) const { return list[static_cast<std::size_t>(k) - 1].first; }
    Entries entries() const {
        Entries out;
        for (const auto& [id, q] : list) out.push_back({id, q});
        return out;
    }
};

Op opP(long long id, long long q) { return Put{id, q}; }
Op opD(long long id, long long q) { return Delete{id, q}; }
Op opC(long long id) { return CountUpTo{id}; }
Op opQ(long long id) { return QtyUpTo{id}; }
Op opA(int k) { return IdAt{k}; }  // helpers: braces inside a CHECK_EQ argument would be split at the commas by the preprocessor

std::vector<long long> ids_of(const Entries& es) {
    std::vector<long long> out;
    for (const Entry& e : es) out.push_back(e.id);
    return out;
}

}  // namespace

// ================================================ Part 1: semantics

TEST(empty_sequence, "part1,edge") {
    OrderSequence s;
    CHECK_EQ(s.size(), 0);
    CHECK_EQ(s.total_qty(), 0);
    CHECK_EQ(s.entries().size(), 0);
    CHECK_THROWS_AS(s.count_up_to(1), UnknownId);
    CHECK_THROWS_AS(s.qty_up_to(1), UnknownId);
    CHECK_THROWS_AS(s.id_at(1), std::out_of_range);
}

TEST(prefix_queries_follow_insertion_order_not_id_order, "part1") {
    OrderSequence s;
    s.put(10, 3);
    s.put(5, 4);
    s.put(7, 5);
    CHECK_EQ(s.count_up_to(10), 1);
    CHECK_EQ(s.count_up_to(5), 2);
    CHECK_EQ(s.count_up_to(7), 3);
    CHECK_EQ(s.qty_up_to(10), 3);
    CHECK_EQ(s.qty_up_to(5), 7);
    CHECK_EQ(s.qty_up_to(7), 12);
    CHECK_EQ(s.id_at(1), 10);
    CHECK_EQ(s.id_at(2), 5);
    CHECK_EQ(s.id_at(3), 7);
    CHECK_EQ(s.total_qty(), 12);
}

TEST(delete_removes_and_reinsert_goes_to_the_end, "part1") {
    OrderSequence s;
    s.put(1, 3);
    s.put(2, 4);
    s.put(3, 5);
    CHECK_EQ(s.remove(2, 4), 0);  // whole order -> nothing left
    CHECK_EQ(s.size(), 2);
    CHECK_EQ(s.count_up_to(3), 2);
    CHECK_EQ(s.qty_up_to(3), 8);
    CHECK_EQ(s.id_at(2), 3);
    CHECK_THROWS_AS(s.count_up_to(2), UnknownId);
    s.put(2, 9);  // the same id again: it goes to the end
    CHECK_EQ(s.count_up_to(2), 3);
    CHECK_EQ(s.qty_up_to(2), 17);
    const Entries expected{{1, 3}, {3, 5}, {2, 9}};
    CHECK_EQ(s.entries(), expected);
}

TEST(invalid_arguments_leave_state_untouched, "part1,edge") {
    OrderSequence s;
    s.put(1, 5);
    CHECK_THROWS_AS(s.put(2, 0), std::invalid_argument);
    CHECK_THROWS_AS(s.put(2, -1), std::invalid_argument);
    CHECK_THROWS_AS(s.put(1, 3), std::invalid_argument);  // id already live
    CHECK_THROWS_AS(s.remove(1, 0), std::invalid_argument);
    CHECK_THROWS_AS(s.remove(1, -2), std::invalid_argument);
    CHECK_THROWS_AS(s.remove(1, 6), std::invalid_argument);  // more than what is left
    CHECK_THROWS_AS(s.remove(99, 1), UnknownId);
    CHECK_THROWS_AS(s.id_at(0), std::out_of_range);
    CHECK_THROWS_AS(s.id_at(2), std::out_of_range);
    CHECK_THROWS_AS(s.id_at(-3), std::out_of_range);
    const Entries expected{{1, 5}};
    CHECK_EQ(s.entries(), expected);
    CHECK_EQ(s.total_qty(), 5);
}

TEST(any_long_is_a_valid_id, "part1,edge") {
    OrderSequence s;
    for (long long id : {0LL, -1LL, LLONG_MIN, LLONG_MAX}) s.put(id, 2);
    CHECK_EQ(s.count_up_to(LLONG_MAX), 4);
    CHECK_EQ(s.count_up_to(0), 1);  // 0 is the first
    CHECK_EQ(s.id_at(3), LLONG_MIN);
    CHECK_EQ(s.remove(0, 2), 0);
    CHECK_EQ(s.count_up_to(LLONG_MAX), 3);
}

TEST(total_quantity_overflow_is_rejected, "part1,edge") {
    OrderSequence s;
    s.put(1, LLONG_MAX - 10);
    CHECK_THROWS_AS(s.put(2, 11), std::overflow_error);
    CHECK_EQ(s.size(), 1);  // unchanged
    s.put(2, 10);           // exactly at the top
    CHECK_EQ(s.qty_up_to(2), LLONG_MAX);
    CHECK_EQ(s.total_qty(), LLONG_MAX);
    CHECK_EQ(s.remove(1, LLONG_MAX - 10), 0);
    s.put(3, 100);  // room again
    CHECK_EQ(s.qty_up_to(3), 110);
}

TEST(sample_script, "part1,fmt") {
    const auto out = OrderSequence::replay(lines("# sample\nPUT 10 5\nPUT 20 3\nPUT 30 7\nCOUNT 30\nQTY 20\nDELETE 20 3\nQTY 30\nAT 2\n\n"
                                                 "DELETE 10 5\nput 20 4\nQTY 20\nDELETE 99 1\nDELETE 30 9\nPUT 30 1\nAT 3\nAT 2\n"));
    CHECK_EQ(out, lines("OK\nOK\nOK\n3\n8\n0\n12\n30\n0\nOK\n11\nERR unknown id\nERR quantity exceeds remaining\nERR duplicate id\nERR index out of range\n20\n"));
}

TEST(parse_rejects_malformed_lines, "part1,fmt") {
    for (const char* bad : {"", "  ", "NOPE 1", "PUT 1", "PUT 1 2 3", "PUT a 2", "PUT 1 2.5", "DELETE 1", "COUNT", "COUNT 1 2", "QTY x", "AT",
                            "AT 99999999999", "AT 1.5", "PUT 99999999999999999999 1"})
        CHECK_THROWS_AS(OrderSequence::parse(bad), std::invalid_argument, std::string("'") + bad + "'");
}

TEST(parse_and_render_every_kind, "part1,fmt") {
    CHECK_EQ(OrderSequence::parse(" put  1   2 "), opP(1, 2));
    CHECK_EQ(OrderSequence::parse("DELETE 1 2"), opD(1, 2));
    CHECK_EQ(OrderSequence::parse("count -3"), opC(-3));
    CHECK_EQ(OrderSequence::parse("QTY 4"), opQ(4));
    CHECK_EQ(OrderSequence::parse("At 5"), opA(5));
    CHECK_EQ(OrderSequence::render(Ok{}), "OK");
    CHECK_EQ(OrderSequence::render(Num{-7}), "-7");
    CHECK_EQ(OrderSequence::render(Err{"boom"}), "ERR boom");
    try {
        OrderSequence::replay({"PUT 1 1", "", "PUT x 1"});
        CHECK(false, "replay should have thrown");
    } catch (const std::invalid_argument& e) {
        CHECK(std::string(e.what()).starts_with("line 3"), e.what());
    }
}

TEST(entries_are_a_plain_ordered_vector, "part1") {
    OrderSequence s;
    s.put(4, 1);
    s.put(2, 2);
    s.put(9, 3);
    const auto es = s.entries();
    CHECK_EQ(es.front().id, 4);
    CHECK_EQ(es.back().id, 9);
    const std::vector<long long> reversed{9, 2, 4};
    CHECK_EQ(ids_of(Entries(es.rbegin(), es.rend())), reversed);
}

// ================================================ Part 2: sub-linear queries

TEST(differential_against_naive_model, "part2,edge") {
    std::mt19937_64 rnd(0);
    OrderSequence s;
    Model m;
    long long next_id = 1;
    for (int step = 0; step < 40'000; ++step) {
        const int dice = static_cast<int>(rnd() % 10);
        if (dice < 4 || m.list.empty()) {
            const long long q = 1 + static_cast<long long>(rnd() % 1000);
            s.put(next_id, q);
            m.put(next_id++, q);
        } else if (dice < 6) {
            const auto [id, q] = m.list[rnd() % m.list.size()];
            CHECK_EQ(s.remove(id, q), m.remove(id, q));  // Part 2 removes whole orders only
        } else {
            const long long id = m.list[rnd() % m.list.size()].first;
            CHECK_EQ(s.count_up_to(id), m.count(id));
            CHECK_EQ(s.qty_up_to(id), m.qty(id));
            const int k = 1 + static_cast<int>(rnd() % m.list.size());
            CHECK_EQ(s.id_at(k), m.id_at(k));
        }
        CHECK_EQ(s.size(), m.list.size());
        if (step % 5000 == 0) CHECK_EQ(s.entries(), m.entries());
    }
    CHECK_EQ(s.entries(), m.entries());
}

TEST(id_at_walks_every_rank_after_many_holes, "part2") {
    OrderSequence s;
    std::mt19937_64 rnd(0);
    std::vector<long long> live;
    for (long long id = 1; id <= 3000; ++id) {
        s.put(id, 1 + id % 7);
        live.push_back(id);
    }
    for (int i = 0; i < 2000; ++i) {
        const std::size_t at = rnd() % live.size();
        const long long id = live[at];
        live.erase(live.begin() + static_cast<std::ptrdiff_t>(at));
        s.remove(id, 1 + id % 7);
    }
    CHECK_EQ(s.size(), 1000);
    for (std::size_t k = 1; k <= live.size(); ++k) {
        CHECK_EQ(s.id_at(static_cast<int>(k)), live[k - 1]);
        CHECK_EQ(s.count_up_to(live[k - 1]), k);
    }
}

TEST(every_small_size_every_prefix, "part2,edge") {
    // Fenwick bugs live at "size is not a power of two", "only the head left", "only the tail left": every n from 1 to 70.
    for (int n = 1; n <= 70; ++n) {
        OrderSequence s;
        for (int i = 1; i <= n; ++i) s.put(100 + i, i);
        for (int i = 1; i <= n; ++i) {
            CHECK_EQ(s.count_up_to(100 + i), i);
            CHECK_EQ(s.qty_up_to(100 + i), static_cast<long long>(i) * (i + 1) / 2);
            CHECK_EQ(s.id_at(i), 100 + i);
        }
        if (n >= 2) {
            s.remove(101, 1);        // drop the head
            s.remove(100 + n, n);    // drop the tail
            CHECK_EQ(s.size(), static_cast<std::size_t>(n - 2));
            if (n >= 3) {
                CHECK_EQ(s.count_up_to(102), 1);
                CHECK_EQ(s.qty_up_to(102), 2);
                CHECK_EQ(s.id_at(1), 102);
            }
        }
    }
}

TEST(half_a_million_orders_and_queries, "part2,perf") {
    std::mt19937_64 rnd(0);
    const int n = 500'000;
    std::vector<long long> qtys(static_cast<std::size_t>(n) + 1);
    std::vector<char> alive(static_cast<std::size_t>(n) + 1, 0);
    OrderSequence s;
    long long acc = 0;
    CHECK_WITHIN_MS(2000, {
        for (int id = 1; id <= n; ++id) {
            qtys[static_cast<std::size_t>(id)] = 1 + static_cast<long long>(rnd() % 100);
            alive[static_cast<std::size_t>(id)] = 1;
            s.put(id, qtys[static_cast<std::size_t>(id)]);
        }
        for (int i = 0; i < n; ++i) {
            const int id = 1 + static_cast<int>(rnd() % static_cast<unsigned>(n));
            if (!alive[static_cast<std::size_t>(id)]) continue;
            if (i % 5 == 0) {
                s.remove(id, qtys[static_cast<std::size_t>(id)]);
                alive[static_cast<std::size_t>(id)] = 0;
            } else {
                acc += s.count_up_to(id) + s.qty_up_to(id) + s.id_at(1 + static_cast<int>(rnd() % s.size()));
            }
        }
    });
    CHECK_GT(acc, 0);
    CHECK_LT(s.size(), static_cast<std::size_t>(n));
}

// ================================================ Part 3: partial removal + compaction

TEST(partial_delete_keeps_position_and_count, "part3") {
    OrderSequence s;
    s.put(1, 10);
    s.put(2, 10);
    s.put(3, 10);
    CHECK_EQ(s.remove(2, 4), 6);
    CHECK_EQ(s.count_up_to(3), 3);  // only reduced: the order is still there
    CHECK_EQ(s.qty_up_to(3), 26);
    CHECK_EQ(s.qty_up_to(2), 16);
    CHECK_EQ(s.total_qty(), 26);
    const Entries after_partial{{1, 10}, {2, 6}, {3, 10}};
    CHECK_EQ(s.entries(), after_partial);
    CHECK_EQ(s.remove(2, 6), 0);  // the rest -> the order is removed
    CHECK_EQ(s.count_up_to(3), 2);
    CHECK_EQ(s.qty_up_to(3), 20);
    CHECK_THROWS_AS(s.remove(2, 1), UnknownId);
    CHECK_THROWS_AS(s.remove(3, 11), std::invalid_argument);
    CHECK_EQ(s.id_at(2), 3);
}

TEST(partial_delete_sample_script, "part3,fmt") {
    CHECK_EQ(OrderSequence::replay(lines("PUT 1 10\nPUT 2 10\nPUT 3 10\nDELETE 2 4\nQTY 3\nCOUNT 3\nDELETE 2 6\nCOUNT 3\nAT 2\n")),
             lines("OK\nOK\nOK\n6\n26\n3\n0\n2\n3\n"));
}

TEST(capacity_is_a_power_of_two_and_validated, "part3,edge") {
    CHECK_EQ(OrderSequence().capacity(), 16);
    CHECK_EQ(OrderSequence(5).capacity(), 8);
    CHECK_EQ(OrderSequence(8).capacity(), 8);
    CHECK_EQ(OrderSequence(1).capacity(), 1);
    CHECK_THROWS_AS(OrderSequence(0), std::invalid_argument);
    CHECK_THROWS_AS(OrderSequence(-4), std::invalid_argument);
}

TEST(full_index_space_triggers_compaction_that_keeps_order, "part3") {
    OrderSequence s(8);
    for (long long id = 1; id <= 8; ++id) s.put(id, id);
    for (long long id = 1; id <= 8; id += 2) s.remove(id, id);  // drop 1,3,5,7 -> four holes
    CHECK_EQ(s.compactions(), 0);
    s.put(9, 9);  // index 9 > 8: must compact
    CHECK_EQ(s.compactions(), 1);
    CHECK_EQ(s.capacity(), 8);  // four live orders: no need to grow
    const std::vector<long long> order{2, 4, 6, 8, 9};
    CHECK_EQ(ids_of(s.entries()), order);
    CHECK_EQ(s.count_up_to(9), 5);
    CHECK_EQ(s.qty_up_to(9), 2 + 4 + 6 + 8 + 9);
    CHECK_EQ(s.id_at(3), 6);
    CHECK_EQ(s.count_up_to(4), 2);
}

TEST(compaction_grows_when_everything_is_alive, "part3") {
    OrderSequence s(8);
    for (long long id = 1; id <= 9; ++id) s.put(id, 1);
    CHECK_EQ(s.compactions(), 1);
    CHECK_EQ(s.capacity(), 16);  // 8 live orders and no holes: it must grow
    CHECK_EQ(s.count_up_to(9), 9);
    for (long long id = 10; id <= 300; ++id) s.put(id, 1);
    CHECK_EQ(s.size(), 300);
    CHECK_EQ(s.count_up_to(300), 300);
    CHECK_EQ(s.id_at(150), 150);
    CHECK(s.capacity() >= 300 && s.capacity() <= 1024, "capacity " + std::to_string(s.capacity()));
}

TEST(compaction_shrinks_back_after_a_burst, "part3,edge") {
    OrderSequence s(16);
    for (long long id = 1; id <= 4000; ++id) s.put(id, 1);
    const int big = s.capacity();
    CHECK_GE(big, 4000);
    for (long long id = 1; id <= 3990; ++id) s.remove(id, 1);
    for (long long id = 5000; id < 5000 + big; ++id) {  // keep putting until a compaction happens
        s.put(id, 1);
        s.remove(id, 1);
    }
    CHECK(s.capacity() < big / 4, "capacity " + std::to_string(s.capacity()) + " after shrink, was " + std::to_string(big));
    CHECK_EQ(s.size(), 10);
    CHECK_EQ(s.count_up_to(4000), 10);
    CHECK_EQ(s.id_at(1), 3991);
}

TEST(differential_with_tiny_capacity_and_partial_deletes, "part3,edge") {
    std::mt19937_64 rnd(0);
    OrderSequence s(4);
    Model m;
    long long next_id = 1;
    for (int step = 0; step < 60'000; ++step) {
        const int dice = static_cast<int>(rnd() % 10);
        if (dice < 4 || m.list.empty()) {
            const long long q = 1 + static_cast<long long>(rnd() % 50);
            s.put(next_id, q);
            m.put(next_id++, q);
        } else if (dice < 8) {
            const auto [id, have] = m.list[rnd() % m.list.size()];
            const long long q = (rnd() & 1) ? have : 1 + static_cast<long long>(rnd() % static_cast<unsigned long long>(have));  // half whole, half partial
            CHECK_EQ(s.remove(id, q), m.remove(id, q));
        } else {
            const long long id = m.list[rnd() % m.list.size()].first;
            CHECK_EQ(s.count_up_to(id), m.count(id));
            CHECK_EQ(s.qty_up_to(id), m.qty(id));
            const int k = 1 + static_cast<int>(rnd() % m.list.size());
            CHECK_EQ(s.id_at(k), m.id_at(k));
        }
        CHECK_EQ(s.size(), m.list.size());
    }
    CHECK_EQ(s.entries(), m.entries());
    CHECK_GT(s.compactions(), 10);
}

TEST(two_million_put_delete_cycles_stay_in_bounded_memory, "part3,perf") {
    OrderSequence s;
    std::deque<long long> window;
    std::mt19937_64 rnd(0);
    const int n = 2'000'000;
    std::vector<long long> qtys(static_cast<std::size_t>(n) + 1);
    CHECK_WITHIN_MS(2000, {
        for (int id = 1; id <= n; ++id) {
            qtys[static_cast<std::size_t>(id)] = 1 + static_cast<long long>(rnd() % 100);
            s.put(id, qtys[static_cast<std::size_t>(id)]);
            window.push_back(id);
            if (window.size() > 1000) {
                const long long old = window.front();  // always remove the oldest: every hole piles up at the front
                window.pop_front();
                s.remove(old, qtys[static_cast<std::size_t>(old)]);
            }
        }
    });
    CHECK_EQ(s.size(), 1000);
    CHECK_LE(s.capacity(), 4096);  // memory follows the live orders, not the two million
    CHECK_GT(s.compactions(), 100);
    CHECK_EQ(s.count_up_to(window.back()), 1000);
    CHECK_EQ(s.id_at(1), window.front());
    CHECK_LE(s.index_buckets(), 4u * static_cast<std::size_t>(s.capacity()));
}

// ================================================ C++-only edge cases (tag "cpp")

TEST(moved_from_sequence_is_a_valid_empty_sequence, "cpp,edge") {
    // The compiler-generated move would copy capacity_/next_index_ (they are ints) but steal the vectors: the moved-from object
    // would then index into empty storage on the next put.
    OrderSequence a(8);
    for (long long id = 1; id <= 5; ++id) a.put(id, id);
    OrderSequence b = std::move(a);
    CHECK_EQ(b.size(), 5);
    CHECK_EQ(b.qty_up_to(5), 15);
    CHECK_EQ(a.size(), 0);  // NOLINT: deliberate use after move
    CHECK_EQ(a.total_qty(), 0);
    CHECK_EQ(a.entries().size(), 0);
    CHECK_THROWS_AS(a.count_up_to(1), UnknownId);
    CHECK_THROWS_AS(a.id_at(1), std::out_of_range);
    a.put(42, 7);  // must work, and must not touch b
    CHECK_EQ(a.id_at(1), 42);
    CHECK_EQ(a.qty_up_to(42), 7);
    CHECK_EQ(b.size(), 5);
    OrderSequence c;
    c = std::move(b);
    CHECK_EQ(c.id_at(5), 5);
    CHECK_EQ(b.size(), 0);  // NOLINT
    b.put(1, 1);
    CHECK_EQ(b.count_up_to(1), 1);
}

TEST(copies_are_deep_and_independent, "cpp") {
    OrderSequence a(4);
    for (long long id = 1; id <= 3; ++id) a.put(id, 10);
    OrderSequence b = a;
    b.remove(1, 10);
    b.put(9, 1);
    CHECK_EQ(a.size(), 3);
    CHECK_EQ(a.count_up_to(3), 3);
    CHECK_EQ(b.size(), 3);
    CHECK_EQ(b.id_at(1), 2);
    OrderSequence c(64);
    c = a;
    a.put(7, 7);
    CHECK_EQ(c.size(), 3);
    CHECK_EQ(a.size(), 4);
    CHECK_THROWS_AS(c.count_up_to(7), UnknownId);
}

TEST(looking_up_an_unknown_id_never_inserts_it, "cpp,edge") {
    // `index_of_[id]` on a missing key INSERTS a default element: the lookup "succeeds" with index 0 and size() grows.
    OrderSequence s;
    CHECK_THROWS_AS(s.count_up_to(99), UnknownId);
    CHECK_THROWS_AS(s.qty_up_to(99), UnknownId);
    CHECK_THROWS_AS(s.remove(99, 1), UnknownId);
    CHECK_EQ(s.size(), 0);
    CHECK_NOTHROW(s.put(99, 1));  // not "duplicate id"
    CHECK_EQ(s.size(), 1);
    s.remove(99, 1);
    CHECK_THROWS_AS(s.count_up_to(99), UnknownId);  // a removed id is unknown again
    CHECK_EQ(s.size(), 0);
}

TEST(failed_calls_leave_no_trace, "cpp,edge") {
    // The overflow check must come BEFORE a compaction: a failed put must not even bump compactions() or change capacity().
    OrderSequence s(2);
    s.put(1, LLONG_MAX - 10);
    s.put(2, 5);  // index space (2) is now full
    CHECK_THROWS_AS(s.put(3, 11), std::overflow_error);
    CHECK_EQ(s.compactions(), 0);
    CHECK_EQ(s.capacity(), 2);
    CHECK_THROWS_AS(s.put(2, 1), std::invalid_argument);  // duplicate, also checked before compacting
    CHECK_EQ(s.compactions(), 0);
    CHECK_THROWS_AS(s.put(3, 0), std::invalid_argument);
    CHECK_EQ(s.compactions(), 0);
    const Entries expected{{1, LLONG_MAX - 10}, {2, 5}};
    CHECK_EQ(s.entries(), expected);
    CHECK_EQ(s.total_qty(), LLONG_MAX - 5);
    s.remove(1, 1);  // partial removal frees quantity
    CHECK_NOTHROW(s.put(3, 6));  // now the sum is exactly LLONG_MAX (and compaction runs)
    CHECK_EQ(s.total_qty(), LLONG_MAX);
    CHECK_EQ(s.compactions(), 1);
}

TEST(total_may_be_exactly_the_maximum_and_back_down, "cpp,edge") {
    OrderSequence s;
    s.put(1, LLONG_MAX);
    CHECK_THROWS_AS(s.put(2, 1), std::overflow_error);
    CHECK_EQ(s.remove(1, 1), LLONG_MAX - 1);
    CHECK_NOTHROW(s.put(2, 1));
    CHECK_EQ(s.qty_up_to(2), LLONG_MAX);
    CHECK_EQ(s.qty_up_to(1), LLONG_MAX - 1);
    CHECK_EQ(s.remove(1, LLONG_MAX - 1), 0);
    CHECK_EQ(s.qty_up_to(2), 1);
}

TEST(index_argument_covers_the_whole_int_range, "cpp,edge") {
    OrderSequence s;
    s.put(1, 1);
    for (int k : {INT_MIN, INT_MIN + 1, -1, 0, 2, INT_MAX - 1, INT_MAX}) CHECK_THROWS_AS(s.id_at(k), std::out_of_range, "k=" + std::to_string(k));
    CHECK_EQ(s.id_at(1), 1);
    CHECK_THROWS_AS(OrderSequence(INT_MAX), std::invalid_argument);
    CHECK_THROWS_AS(OrderSequence((1 << 29) + 1), std::invalid_argument);
    CHECK_THROWS_AS(OrderSequence(INT_MIN), std::invalid_argument);
}

TEST(from_chars_prefix_and_sign_traps, "cpp,edge") {
    // std::from_chars("12abc") succeeds with 12 and a pointer into the middle; "+1" fails; "0x10" stops after "0".
    for (const char* bad : {"PUT 12abc 1", "PUT 1 2x", "PUT +1 2", "PUT 1 +2", "COUNT 1e3", "AT 0x10", "AT 3x", "AT +1", "QTY --1", "COUNT 1_000", "DELETE 1 1 "
                            "1"})
        CHECK_THROWS_AS(OrderSequence::parse(bad), std::invalid_argument, std::string("'") + bad + "'");
    CHECK_EQ(OrderSequence::parse("COUNT -9223372036854775808"), opC(LLONG_MIN));
    CHECK_EQ(OrderSequence::parse("PUT 9223372036854775807 9223372036854775807"), opP(LLONG_MAX, LLONG_MAX));
    CHECK_THROWS_AS(OrderSequence::parse("COUNT 9223372036854775808"), std::invalid_argument);  // LLONG_MAX + 1
    CHECK_EQ(OrderSequence::parse("AT 2147483647"), opA(INT_MAX));
    CHECK_THROWS_AS(OrderSequence::parse("AT 2147483648"), std::invalid_argument);
    CHECK_EQ(OrderSequence::parse("PUT 007 0010"), opP(7, 10));  // leading zeros are decimal, not octal
}

TEST(bytes_above_127_and_nul_in_commands, "cpp,edge") {
    // std::toupper / std::isspace on a negative char is UB; these must simply be rejected.
    CHECK_THROWS_AS(OrderSequence::parse("\xC3\xA9T 1 2"), std::invalid_argument);
    CHECK_THROWS_AS(OrderSequence::parse("PUT \xFF 2"), std::invalid_argument);
    CHECK_THROWS_AS(OrderSequence::parse(std::string_view("PUT 1\0 2", 8)), std::invalid_argument);
    CHECK_EQ(OrderSequence::parse("\tput\t1\t2\r\n"), opP(1, 2));
}

TEST(business_errors_become_err_but_the_text_is_exact, "cpp,fmt") {
    const auto out = OrderSequence::replay(lines("PUT 1 9223372036854775807\nPUT 2 1\nPUT 2 0\nPUT 1 1\nDELETE 1 0\nDELETE 3 1\nDELETE 1 9223372036854775807\n"
                                                 "AT -2147483648\nCOUNT 5\nQTY 5\n"));
    CHECK_EQ(out, lines("OK\nERR overflow\nERR invalid quantity\nERR duplicate id\nERR invalid quantity\nERR unknown id\n0\nERR index out of range\n"
                        "ERR unknown id\nERR unknown id\n"));
    CHECK_EQ(OrderSequence::replay({"\r", "  # c", "PUT 1 2\r"}).size(), 1);
}

TEST(index_map_memory_follows_the_live_orders, "cpp,edge") {
    // std::unordered_map never gives bucket memory back on its own; compaction must rehash it down.
    OrderSequence s(16);
    for (long long id = 1; id <= 100'000; ++id) s.put(id, 1);
    const std::size_t big_buckets = s.index_buckets();
    CHECK_GE(big_buckets, 100'000u);
    for (long long id = 1; id <= 99'990; ++id) s.remove(id, 1);
    for (long long id = 200'000; id < 200'000 + 200'000; ++id) {  // churn until compaction has happened
        s.put(id, 1);
        s.remove(id, 1);
    }
    CHECK_LE(s.capacity(), 64);
    CHECK_LT(s.index_buckets(), big_buckets / 100);
    CHECK_EQ(s.size(), 10);
    CHECK_EQ(s.id_at(1), 99'991);
}

TEST(capacity_is_always_a_power_of_two, "cpp") {
    std::mt19937_64 rnd(5);
    OrderSequence s(3);
    CHECK(std::has_single_bit(static_cast<unsigned>(s.capacity())));
    std::deque<long long> live;
    long long next_id = 1;
    for (int step = 0; step < 20'000; ++step) {
        if (live.empty() || rnd() % 3 != 0) {
            s.put(next_id, 1);
            live.push_back(next_id++);
        } else {
            s.remove(live.front(), 1);
            live.pop_front();
        }
        CHECK(std::has_single_bit(static_cast<unsigned>(s.capacity())), "step " + std::to_string(step));
        CHECK_GE(s.capacity(), 3);
    }
}

TEST(strided_ids_do_not_degrade_the_index, "cpp,perf") {
    // Identity hash + power-of-two stride is the classic way to put every key in one bucket (with a power-of-two bucket array).
    OrderSequence s;
    const int n = 200'000;
    CHECK_WITHIN_MS(2000, {
        for (int i = 0; i < n; ++i) s.put(static_cast<long long>(i) << 32, 1);
        for (int i = 0; i < n; ++i) CHECK_EQ(s.count_up_to(static_cast<long long>(i) << 32), i + 1);
    });
}

MT_MAIN()
