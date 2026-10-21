// oa01 · Job Chain report — C++20 starter.  Statement: ../problem.md.  Replace every TODO.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>` and run `... run <dir> --impl work`.
#pragma once

#include <istream>
#include <ostream>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

namespace jobchains {

/// One input row.  An aggregate: ==, copy and move are generated.  Hint: there is no compact constructor in C++, so write
/// a validate(const Job&) and call it from parse() AND chains() (a Job can be built by hand with garbage in it).
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
    long long average_seconds() const { throw std::logic_error("TODO"); }  // truncating division
    friend bool operator==(const Chain&, const Chain&) = default;
};

struct MalformedInput : std::runtime_error {
    using std::runtime_error::runtime_error;
};

/// A closed sum type: the C++ counterpart of a sealed interface.
struct Ok { std::vector<Chain> chains; };
struct Malformed { std::string reason; };
using Outcome = std::variant<Ok, Malformed>;

/// Part 1: skip '#' lines and blank lines; every other line is exactly three base-10 integers separated by commas.
/// Hints: std::from_chars (and check the end pointer), never std::stoi; do not call std::isspace on a plain char.
inline std::vector<Job> parse(const std::vector<std::string>&) { throw std::logic_error("TODO"); }

/// Part 1: seconds -> "hh:mm:ss"; hours at least two digits, never wrapped.
inline std::string hhmmss(long long) { throw std::logic_error("TODO"); }

/// Part 2: stitch jobs into chains, enforce the cross-row rules, sort (runtime desc, start_job asc).
/// Hint: signed overflow is undefined behaviour; __builtin_add_overflow tells you instead.
inline std::vector<Chain> chains(const std::vector<Job>&) { throw std::logic_error("TODO"); }

/// Part 3: MalformedInput exception -> Malformed value.
inline Outcome analyze(const std::vector<std::string>&) { throw std::logic_error("TODO"); }

/// Part 3: render the report.  Hint: std::visit with an overloaded set of lambdas.
inline std::vector<std::string> render(const Outcome&) { throw std::logic_error("TODO"); }

inline std::vector<std::string> solve(const std::vector<std::string>& lines) { return render(analyze(lines)); }

/// stdin -> stdout driver (given).  Exit status is 0 even for Malformed Input, as the statement demands.
inline int run(std::istream& in, std::ostream& out) {
    std::vector<std::string> lines;
    for (std::string line; std::getline(in, line);) lines.push_back(std::move(line));
    for (const std::string& l : solve(lines)) out << l << '\n';
    return 0;
}

}  // namespace jobchains
