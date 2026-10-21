// How to answer "how do you know it is faster": same update stream into each table, warm up, best of five, print ns/op.
// `reference.hpp` is the code of the lecture.  Build with -O2 and no sanitizers.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../../../../loop/rounds/01_video/hc07_ticker_hash_map/cpp/reference.hpp"

using namespace tickers;
using Clock = std::chrono::steady_clock;

template <class F>
double best_ns_per_op(std::size_t ops, F run) {
    run();  // warm-up: caches, branch predictors, page faults
    double best = 1e18;
    for (int round = 0; round < 5; ++round) {
        const auto t0 = Clock::now();
        run();
        const auto t1 = Clock::now();
        best = std::min(best, std::chrono::duration<double, std::nano>(t1 - t0).count() / static_cast<double>(ops));
    }
    return best;
}

int main() {
    constexpr std::size_t kOps = 20'000'000;
    std::mt19937_64 rng(1);
    for (std::size_t universe_size : {8000u, 2'000'000u}) {
        std::unordered_set<std::string> seen;
        std::vector<std::string> names;
        while (names.size() < universe_size) {
            std::string s;
            const int len = 3 + static_cast<int>(rng() % 6);
            for (int i = 0; i < len; ++i) s.push_back(static_cast<char>('A' + rng() % 26));
            if (seen.insert(s).second) names.push_back(s);
        }
        std::vector<Key> keys;
        for (const auto& n : names) keys.push_back(codec::pack(n));
        std::vector<std::uint32_t> picks(1 << 20);  // the access pattern is generated once, outside the timed loops
        for (auto& p : picks) p = static_cast<std::uint32_t>(rng() % universe_size);
        const std::size_t mask = picks.size() - 1;

        std::unordered_map<std::string, long long> stl;
        TickerMap strmap(universe_size);
        LongTickerMap longmap(universe_size);
        FrozenTickerMap frozen(names);
        std::vector<int> index;
        for (Key k : keys) index.push_back(frozen.index_of(k));
        for (std::size_t i = 0; i < universe_size; ++i) { stl[names[i]] = 0; strmap.put(names[i], 0); longmap.put(keys[i], 0); }

        std::cout << universe_size << " tickers, " << kOps << " updates per round\n";
        auto report = [](const char* what, double ns) { std::cout << "  " << std::left << std::setw(30) << what << std::right << std::fixed << std::setprecision(1) << std::setw(6) << ns << " ns/op\n"; };
        report("std::unordered_map<string>", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) stl.find(names[picks[i & mask]])->second += 1; }));
        report("TickerMap (string_view)", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) strmap.add(names[picks[i & mask]], 1); }));
        report("LongTickerMap (packed key)", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) longmap.add(keys[picks[i & mask]], 1); }));
        report("FrozenTickerMap::add(key)", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) frozen.add(keys[picks[i & mask]], 1); }));
        report("FrozenTickerMap::add_at(index)", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) frozen.add_at(index[picks[i & mask]], 1); }));
    }
}
