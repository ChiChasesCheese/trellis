// oa01 · Job Chain report — C++20 reference.  Statement: ../problem.md (verbatim original: mock_maven/catalog/raw/hackerrank_job_runner_photos.md).
// Same Parts as the Java suite: 1 = parse + hhmmss, 2 = chains, 3 = analyze/render/run.
#pragma once

#include <algorithm>
#include <charconv>
#include <cstdio>
#include <istream>
#include <ostream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <variant>
#include <vector>

namespace jobchains {

/// One input row.  A plain aggregate: the compiler writes ==, copy and move.  Unlike a Java record there is no compact
/// constructor to validate it, so the rules live in validate() and every entry point calls it.
struct Job {
    int id;
    long long runtime_seconds;
    int next_id;
    friend bool operator==(const Job&, const Job&) = default;
};

struct Chain {
    int start_job;
    int last_job;
    int count;
    long long total_seconds;
    long long average_seconds() const { return total_seconds / count; }  // integer division truncates toward zero; total >= 0 and count >= 1
    friend bool operator==(const Chain&, const Chain&) = default;
};

struct MalformedInput : std::runtime_error {
    using std::runtime_error::runtime_error;
};

/// Result of analyze(): a closed sum type.  std::variant is the C++ spelling of Java's sealed interface + records.
struct Ok { std::vector<Chain> chains; };
struct Malformed { std::string reason; };
using Outcome = std::variant<Ok, Malformed>;

namespace detail {

template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

// Not std::isspace(char): passing a negative char (any byte >= 0x80 where char is signed) is undefined behaviour.
constexpr bool is_space(char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\v' || c == '\f'; }

constexpr std::string_view trim(std::string_view s) {
    while (!s.empty() && is_space(s.front())) s.remove_prefix(1);
    while (!s.empty() && is_space(s.back())) s.remove_suffix(1);
    return s;
}

// The WHOLE token must be a base-10 integer that fits Int.  std::from_chars never skips whitespace and never accepts a
// leading '+'; unlike std::stoi / strtol it also reports "stopped early" through the returned pointer, which we check.
template <class Int> Int parse_int(std::string_view tok, std::string_view line) {
    Int v{};
    const char* first = tok.data();
    const char* last = tok.data() + tok.size();
    auto [ptr, ec] = std::from_chars(first, last, v);
    if (ec == std::errc::result_out_of_range) throw MalformedInput("number out of range: " + std::string(line));
    if (ec != std::errc{} || ptr != last) throw MalformedInput("bad number '" + std::string(tok) + "' in line: " + std::string(line));
    return v;
}

}  // namespace detail

/// Single-row rules.  Cross-row rules (duplicates, dangling, two predecessors, cycles) live in chains().
inline void validate(const Job& j) {
    if (j.id <= 0) throw MalformedInput("job_id must be positive: " + std::to_string(j.id));
    if (j.runtime_seconds < 0) throw MalformedInput("negative runtime: " + std::to_string(j.runtime_seconds));
    if (j.next_id < 0) throw MalformedInput("negative next_job_id: " + std::to_string(j.next_id));
    if (j.next_id == j.id) throw MalformedInput("self loop: " + std::to_string(j.id));
}

/// Part 1: skip blank lines and '#' lines; every other line is exactly three comma-separated integers.
inline std::vector<Job> parse(const std::vector<std::string>& lines) {
    std::vector<Job> jobs;
    jobs.reserve(lines.size());
    for (const std::string& raw : lines) {
        std::string_view line = detail::trim(raw);
        if (line.empty() || line.front() == '#') continue;
        std::string_view field[3];
        std::size_t begin = 0;
        for (int i = 0; i < 3; ++i) {
            std::size_t comma = line.find(',', begin);
            if (i < 2 ? comma == std::string_view::npos : comma != std::string_view::npos)
                throw MalformedInput("expected exactly 3 fields: " + raw);
            field[i] = detail::trim(line.substr(begin, comma == std::string_view::npos ? comma : comma - begin));
            begin = comma + 1;
        }
        Job j{detail::parse_int<int>(field[0], raw), detail::parse_int<long long>(field[1], raw), detail::parse_int<int>(field[2], raw)};
        validate(j);
        jobs.push_back(j);
    }
    return jobs;
}

/// Part 1: seconds -> hh:mm:ss.  Hours are at least two digits and never wrapped (100:00:00 is fine).
inline std::string hhmmss(long long seconds) {
    if (seconds < 0) throw std::invalid_argument("negative duration: " + std::to_string(seconds));
    char buf[48];
    std::snprintf(buf, sizeof buf, "%02lld:%02lld:%02lld", seconds / 3600, seconds / 60 % 60, seconds % 60);
    return buf;
}

/// Part 2: stitch rows into chains and enforce every cross-row rule.  O(n) expected, no recursion (a million-job chain
/// would overflow the call stack of a recursive walk).
inline std::vector<Chain> chains(const std::vector<Job>& jobs) {
    constexpr std::size_t none = static_cast<std::size_t>(-1);
    const std::size_t n = jobs.size();
    std::unordered_map<int, std::size_t> index_of;
    index_of.reserve(n * 2);
    for (std::size_t i = 0; i < n; ++i) {
        validate(jobs[i]);  // an aggregate can be built invalid by hand
        if (!index_of.emplace(jobs[i].id, i).second) throw MalformedInput("duplicate job_id " + std::to_string(jobs[i].id));
    }
    std::vector<std::size_t> next(n, none);
    std::vector<char> has_predecessor(n, 0);  // vector<bool> is a bit-packed proxy container; char is simpler and faster
    for (std::size_t i = 0; i < n; ++i) {
        if (jobs[i].next_id == 0) continue;
        auto it = index_of.find(jobs[i].next_id);
        if (it == index_of.end()) throw MalformedInput("dangling next_job_id " + std::to_string(jobs[i].next_id));
        if (has_predecessor[it->second]) throw MalformedInput("two jobs point at " + std::to_string(jobs[i].next_id));
        has_predecessor[it->second] = 1;
        next[i] = it->second;
    }
    std::vector<Chain> out;
    std::size_t visited = 0;
    for (std::size_t head = 0; head < n; ++head) {
        if (has_predecessor[head]) continue;
        int count = 0;
        long long total = 0;
        std::size_t cur = head;
        for (;;) {
            ++visited;
            ++count;
            // Signed overflow is undefined behaviour in C++ (Java would wrap, or throw with addExact): detect it.
            if (__builtin_add_overflow(total, jobs[cur].runtime_seconds, &total)) throw MalformedInput("chain runtime overflows 64 bits");
            if (next[cur] == none) break;
            cur = next[cur];
        }
        out.push_back(Chain{jobs[head].id, jobs[cur].id, count, total});
    }
    // Every node has in-degree <= 1 and was walked from a head; a node nobody walked sits on a cycle.
    if (visited != n) throw MalformedInput("cycle among jobs not reachable from a head");
    std::ranges::sort(out, [](const Chain& a, const Chain& b) {
        return a.total_seconds != b.total_seconds ? a.total_seconds > b.total_seconds : a.start_job < b.start_job;
    });
    return out;
}

/// Part 3: the whole analysis; a MalformedInput exception becomes a Malformed value.
inline Outcome analyze(const std::vector<std::string>& lines) {
    try {
        return Ok{chains(parse(lines))};
    } catch (const MalformedInput& e) {
        return Malformed{e.what()};
    }
}

/// Part 3: render.  std::visit needs a branch for every alternative, so adding a third Outcome breaks the build here.
inline std::vector<std::string> render(const Outcome& outcome) {
    return std::visit(detail::overloaded{
        [](const Malformed&) { return std::vector<std::string>{"Malformed Input"}; },
        [](const Ok& ok) {
            std::vector<std::string> lines{"-"};
            for (const Chain& c : ok.chains) {
                lines.push_back("start_job: " + std::to_string(c.start_job));
                lines.push_back("last_job: " + std::to_string(c.last_job));
                lines.push_back("number_of_jobs: " + std::to_string(c.count));
                lines.push_back("job_chain_runtime: " + hhmmss(c.total_seconds));
                lines.push_back("average_job_time: " + hhmmss(c.average_seconds()));
                lines.push_back("-");
            }
            return lines;
        }}, outcome);
}

inline std::vector<std::string> solve(const std::vector<std::string>& lines) { return render(analyze(lines)); }

/// stdin -> stdout driver.  The statement demands exit status 0 even for Malformed Input, so this always returns 0.
inline int run(std::istream& in, std::ostream& out) {
    std::vector<std::string> lines;
    for (std::string line; std::getline(in, line);) lines.push_back(std::move(line));
    for (const std::string& l : solve(lines)) out << l << '\n';
    return 0;
}

}  // namespace jobchains
