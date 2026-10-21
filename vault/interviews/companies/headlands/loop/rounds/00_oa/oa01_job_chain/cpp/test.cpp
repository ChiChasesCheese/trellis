// oa01 · Job Chain report — C++20 tests.  Same cases as test/JobChainsTest.java, plus the C++-only edge cases
// (tagged "cpp": from_chars strictness, high-bit bytes, signed overflow, int range, moved-from/aggregate invalid state).
// Build: python3 tools/cpptest.py run <dir> --impl reference|starter|work
#include <algorithm>
#include <climits>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <variant>
#include <vector>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace jobchains;

namespace jobchains {
std::ostream& operator<<(std::ostream& os, const Job& j) { return os << "Job{" << j.id << "," << j.runtime_seconds << "," << j.next_id << "}"; }
std::ostream& operator<<(std::ostream& os, const Chain& c) {
    return os << "Chain{" << c.start_job << "," << c.last_job << "," << c.count << "," << c.total_seconds << "}";
}
}  // namespace jobchains

using Lines = std::vector<std::string>;

static Lines lines_of(const std::string& block) {
    Lines out;
    std::istringstream in(block);
    for (std::string l; std::getline(in, l);) out.push_back(l);
    return out;
}

static bool rejects_parse(const std::string& row) {
    try { parse({"#h", row}); } catch (const MalformedInput&) { return true; }
    return false;
}

// ================================================ Part 1: parse + hhmmss

TEST(parses_header_blank_lines_and_spaces, "part1") {
    auto jobs = parse(lines_of("#job_id,runtime_in_seconds,next_job_id\n1, 60, 23\n\n23 ,30,0\n"));
    CHECK_EQ(jobs, (std::vector<Job>{{1, 60, 23}, {23, 30, 0}}));
}

TEST(rejects_bad_lines, "part1,edge") {
    for (const char* bad : {"1,2", "1,2,3,4", "a,2,3", "1;2;3", "0,5,0", "-1,5,0", "3,-5,0", "3,5,-1", "4,1,4", "99999999999,1,0"})
        CHECK(rejects_parse(bad), std::string("should be rejected: ") + bad);
}

TEST(formats_durations, "part1,fmt") {
    CHECK_EQ(hhmmss(0), "00:00:00");
    CHECK_EQ(hhmmss(59), "00:00:59");
    CHECK_EQ(hhmmss(60), "00:01:00");
    CHECK_EQ(hhmmss(3661), "01:01:01");
    CHECK_EQ(hhmmss(7200), "02:00:00");  // classic bug: forgetting % 60 prints 02:120:00
    CHECK_EQ(hhmmss(360'000), "100:00:00");
}

// ---- C++-only Part 1 edge cases

TEST(from_chars_strictness_rejects_what_stoi_would_accept, "part1,edge,cpp") {
    // std::stoi("3abc") == 3 and std::stoi(" 3") == 3; strtol also takes '+', hex with base 0, and ignores overflow.
    for (const char* bad : {"1,2,3abc", "1,2,3 4", "+1,2,3", "1,+2,3", "1,2,+3", "0x10,1,0", "1e3,1,0", "1,2.5,0", "1,,3", ",,", "1,2,", ",1,2",
                            "-,1,0", "1,-,0", "1, - 5,0", "1,2,3,", "1_000,1,0", "\xD9\xA1,2,3"})  // last: Arabic-Indic digit one, UTF-8
        CHECK(rejects_parse(bad), std::string("should be rejected: ") + bad);
}

TEST(embedded_nul_and_high_bit_bytes_are_malformed_not_ub, "part1,edge,cpp") {
    // isspace(char) with a negative value is UB; a NUL inside a std::string must not truncate the line either.
    CHECK(rejects_parse(std::string("1,2\0,3", 6)));
    CHECK(rejects_parse(std::string("1,2,3\0", 6)));
    CHECK(rejects_parse("\xC3\xA9,1,0"));
    CHECK(rejects_parse("1,\xFF,0"));
    CHECK(rejects_parse("\xA0" "1,2,3"));  // NBSP-like byte in front: not ASCII whitespace
    CHECK_EQ(parse({"1,2,3\x0b"}).size(), 1u);  // vertical tab is whitespace
}

TEST(crlf_tabs_and_leading_zeros, "part1,edge,cpp") {
    auto jobs = parse({"#job_id,runtime_in_seconds,next_job_id\r", "1,\t60 ,23\r", "\r", "   ", "007,060,000"});
    CHECK_EQ(jobs, (std::vector<Job>{{1, 60, 23}, {7, 60, 0}}));
    CHECK_EQ(parse({"5,-0,0"}), (std::vector<Job>{{5, 0, 0}}));  // "-0" is the integer 0
}

TEST(integer_range_boundaries, "part1,edge,cpp") {
    CHECK_EQ(parse({"2147483647,0,0"})[0].id, INT_MAX);
    CHECK(rejects_parse("2147483648,0,0"));
    CHECK(rejects_parse("1,0,2147483648"));
    CHECK_EQ(parse({"1,9223372036854775807,0"})[0].runtime_seconds, LLONG_MAX);
    CHECK(rejects_parse("1,9223372036854775808,0"));
    CHECK(rejects_parse("1,99999999999999999999999999999999,0"));
    CHECK(rejects_parse("-2147483649,1,0"));
}

TEST(hhmmss_extremes, "part1,edge,fmt,cpp") {
    CHECK_EQ(hhmmss(LLONG_MAX), "2562047788015215:30:07");
    CHECK_EQ(hhmmss(3599), "00:59:59");
    CHECK_EQ(hhmmss(86'399), "23:59:59");
    CHECK_EQ(hhmmss(86'400), "24:00:00");
    CHECK_THROWS_AS(hhmmss(-1), std::invalid_argument);
    CHECK_THROWS_AS(hhmmss(LLONG_MIN), std::invalid_argument);  // -LLONG_MIN would be signed overflow; must be rejected first
}

// ================================================ Part 2: chains

TEST(builds_chains_sorted_by_runtime_desc, "part2") {
    auto cs = chains(parse(lines_of("#job_id,runtime_in_seconds,next_job_id\n1,60,23\n23,30,3\n3,15,0\n5,200,0\n")));
    CHECK_EQ(cs, (std::vector<Chain>{{5, 5, 1, 200}, {1, 3, 3, 105}}));
    CHECK_EQ(cs[1].average_seconds(), 35);
}

TEST(input_order_does_not_matter, "part2,edge") {
    Lines rows{"3,15,0", "1,60,23", "23,30,3"};
    std::reverse(rows.begin(), rows.end());
    CHECK_EQ(chains(parse(rows)), (std::vector<Chain>{{1, 3, 3, 105}}));
}

TEST(tie_breaks_on_start_job, "part2,edge") {
    auto cs = chains(parse({"9,10,0", "4,10,0"}));
    REQUIRE_EQ(cs.size(), 2u);
    CHECK_EQ(cs[0].start_job, 4);
    CHECK_EQ(cs[1].start_job, 9);
}

TEST(rejects_structural_errors, "part2,edge") {
    for (const char* rows : {"1,10,2|2,10,0|1,5,0",   // duplicate id
                             "1,10,7",                // dangling next
                             "1,10,3|2,10,3|3,10,0",  // two predecessors
                             "1,10,2|2,10,1",         // pure cycle, no head
                             "1,10,0|2,10,3|3,10,2"}) {  // good chain + cycle
        std::vector<std::string> v;
        std::istringstream in(rows);
        for (std::string r; std::getline(in, r, '|');) v.push_back(r);
        auto jobs = parse(v);
        CHECK_THROWS_AS(chains(jobs), MalformedInput, rows);
    }
}

TEST(empty_input_has_no_chains, "part2,edge") {
    CHECK_EQ(chains(parse({"#job_id,runtime_in_seconds,next_job_id"})), std::vector<Chain>{});
}

TEST(huge_runtimes_do_not_overflow_int, "part2,edge") {
    auto cs = chains(parse({"1,2000000000,2", "2,2000000000,0"}));
    REQUIRE_EQ(cs.size(), 1u);
    CHECK_EQ(cs[0].total_seconds, 4'000'000'000LL);
}

// ---- C++-only Part 2 edge cases

TEST(chains_revalidates_hand_built_jobs, "part2,edge,cpp") {
    // Job is an aggregate: nothing stops Job{0,..} reaching chains() without going through parse().
    CHECK_THROWS_AS(chains({Job{0, 5, 0}}), MalformedInput);
    CHECK_THROWS_AS(chains({Job{-3, 5, 0}}), MalformedInput);
    CHECK_THROWS_AS(chains({Job{4, 1, 4}}), MalformedInput);
    CHECK_THROWS_AS(chains({Job{1, -1, 0}}), MalformedInput);
    CHECK_THROWS_AS(chains({Job{1, 1, -2}}), MalformedInput);
}

TEST(total_overflow_is_rejected_not_ub, "part2,edge,cpp") {
    // Two LLONG_MAX runtimes: signed addition would be UB (UBSan aborts the whole binary if the code just adds).
    CHECK_THROWS_AS(chains(parse({"1,9223372036854775807,2", "2,1,0"})), MalformedInput);
    CHECK_THROWS_AS(chains(parse({"1,9223372036854775807,2", "2,9223372036854775807,0"})), MalformedInput);
    auto ok = chains(parse({"1,9223372036854775806,2", "2,1,0"}));  // exactly LLONG_MAX: fits
    REQUIRE_EQ(ok.size(), 1u);
    CHECK_EQ(ok[0].total_seconds, LLONG_MAX);
    CHECK_EQ(ok[0].average_seconds(), LLONG_MAX / 2);
}

TEST(average_truncates_toward_zero, "part2,edge,fmt,cpp") {
    CHECK_EQ((Chain{2, 3, 2, 35}).average_seconds(), 17);  // the statement's example: 17.5 -> 17
    CHECK_EQ((Chain{1, 1, 1, 0}).average_seconds(), 0);
    CHECK_EQ((Chain{1, 3, 3, 1}).average_seconds(), 0);
    CHECK_EQ((Chain{1, 2, 2, LLONG_MAX}).average_seconds(), LLONG_MAX / 2);
}

TEST(very_long_chain_does_not_need_recursion, "part2,edge,cpp") {
    // A recursive walk of 1,000,000 nodes needs a stack frame per node; the iterative walk uses O(1) stack.
    const int n = 1'000'000;
    std::vector<Job> jobs;
    jobs.reserve(n);
    for (int i = 1; i <= n; ++i) jobs.push_back(Job{i, 1, i == n ? 0 : i + 1});
    std::reverse(jobs.begin(), jobs.end());
    auto cs = chains(jobs);
    REQUIRE_EQ(cs.size(), 1u);
    CHECK_EQ(cs[0], (Chain{1, n, n, n}));
}

TEST(chains_does_not_modify_its_input_and_is_repeatable, "part2,edge,cpp") {
    const std::vector<Job> jobs = parse({"3,15,0", "1,60,23", "23,30,3", "5,200,0"});
    const auto copy = jobs;
    auto a = chains(jobs);
    auto b = chains(jobs);
    CHECK_EQ(jobs, copy);
    CHECK_EQ(a, b);
}

// ================================================ Part 3: whole report

TEST(renders_report_exactly, "part3,fmt") {
    auto out = solve(lines_of("#job_id,runtime_in_seconds,next_job_id\n1,60,23\n23,30,3\n3,15,0\n5,200,0\n"));
    CHECK_EQ(out, lines_of("-\nstart_job: 5\nlast_job: 5\nnumber_of_jobs: 1\njob_chain_runtime: 00:03:20\naverage_job_time: 00:03:20\n"
                           "-\nstart_job: 1\nlast_job: 3\nnumber_of_jobs: 3\njob_chain_runtime: 00:01:45\naverage_job_time: 00:00:35\n-\n"));
}

TEST(official_hackerrank_example, "part3,fmt") {
    // The example printed in the original statement.
    auto out = solve(lines_of("#job_id,runtime_in_seconds,next_job_id\n1,60,23\n2,23,3\n3,12,0\n23,30,0\n"));
    CHECK_EQ(out, lines_of("-\nstart_job: 1\nlast_job: 23\nnumber_of_jobs: 2\njob_chain_runtime: 00:01:30\naverage_job_time: 00:00:45\n"
                           "-\nstart_job: 2\nlast_job: 3\nnumber_of_jobs: 2\njob_chain_runtime: 00:00:35\naverage_job_time: 00:00:17\n-\n"));
}

TEST(malformed_is_a_single_line, "part3,fmt") {
    auto outcome = analyze({"#h", "1,10,2"});
    CHECK(std::holds_alternative<Malformed>(outcome));
    CHECK_EQ(render(outcome), Lines{"Malformed Input"});
}

// ---- C++-only Part 3 edge cases

TEST(run_is_exit_zero_and_writes_exact_bytes, "part3,fmt,io,cpp") {
    {
        std::istringstream in("garbage");
        std::ostringstream out;
        CHECK_EQ(run(in, out), 0);  // statement: "your program should exit zero"
        CHECK_EQ(out.str(), "Malformed Input\n");
    }
    {
        std::istringstream in("#job_id,runtime_in_seconds,next_job_id\r\n5, 200 ,0\r\n\r\n1,60,23\r\n23,30,3\r\n3,15,0");  // CRLF, no final newline
        std::ostringstream out;
        CHECK_EQ(run(in, out), 0);
        CHECK_EQ(out.str(), "-\nstart_job: 5\nlast_job: 5\nnumber_of_jobs: 1\njob_chain_runtime: 00:03:20\naverage_job_time: 00:03:20\n"
                            "-\nstart_job: 1\nlast_job: 3\nnumber_of_jobs: 3\njob_chain_runtime: 00:01:45\naverage_job_time: 00:00:35\n-\n");
    }
    {
        std::istringstream in("");
        std::ostringstream out;
        CHECK_EQ(run(in, out), 0);
        CHECK_EQ(out.str(), "-\n");  // header-less, row-less input: no chains, still a well-formed report
    }
}

TEST(overflowing_chain_total_prints_malformed_instead_of_crashing, "part3,edge,cpp") {
    CHECK_EQ(solve({"1,9223372036854775807,2", "2,9223372036854775807,0"}), Lines{"Malformed Input"});
}

TEST(outcome_variant_carries_a_reason, "part3,edge,cpp") {
    auto outcome = analyze({"1,2"});
    const auto* m = std::get_if<Malformed>(&outcome);
    REQUIRE(m != nullptr);
    CHECK(!m->reason.empty());
    auto good = analyze({"1,2,0"});
    const auto* ok = std::get_if<Ok>(&good);
    REQUIRE(ok != nullptr);
    CHECK_EQ(ok->chains, (std::vector<Chain>{{1, 1, 1, 2}}));
}

TEST(million_jobs_in_under_two_seconds, "part3,perf") {
    std::mt19937_64 rnd(0);
    const int n = 1'000'000;
    std::vector<int> ids(n);
    std::iota(ids.begin(), ids.end(), 1);
    std::shuffle(ids.begin(), ids.end(), rnd);
    Lines rows;
    rows.reserve(n + 1);
    rows.push_back("#job_id,runtime_in_seconds,next_job_id");
    for (int i = 0; i < n; ++i) {
        bool tail = i == n - 1 || rnd() % 100 == 0;  // about 100 jobs per chain
        rows.push_back(std::to_string(ids[i]) + "," + std::to_string(rnd() % 3600) + "," + std::to_string(tail ? 0 : ids[i + 1]));
    }
    std::shuffle(rows.begin() + 1, rows.end(), rnd);
    Lines out;
    CHECK_WITHIN_MS(2000, out = solve(rows););
    REQUIRE(!out.empty());
    CHECK_EQ(out.front(), "-");
    CHECK_EQ(out.back(), "-");
}

MT_MAIN()
