// SAN: none
// RUN: $BIN gen
// RUN: $BIN cin_sync < /tmp/c15_nums.txt
// RUN: $BIN cin_nosync < /tmp/c15_nums.txt
// RUN: $BIN scanf < /tmp/c15_nums.txt
// RUN: $BIN fread < /tmp/c15_nums.txt
// RUN: $BIN parsers
// C15: where the time goes in input-heavy programs. Modes selected by argv[1].
#include <charconv>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static const char* kPath = "/tmp/c15_nums.txt";
static long N() { return std::getenv("QUICK") ? 20000 : 1'000'000; }

struct Timer {
    const char* name; std::chrono::steady_clock::time_point t0 = std::chrono::steady_clock::now();
    ~Timer() { std::fprintf(stderr, "%-22s %8.1f ms\n", name, std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count()); }
};

int main(int argc, char** argv) {
    std::string mode = argc > 1 ? argv[1] : "";
    if (mode == "gen") {
        std::FILE* f = std::fopen(kPath, "w");
        for (long i = 0; i < N(); ++i) std::fprintf(f, "%ld\n", (i * 2654435761L) % 1000003);
        std::fclose(f);
        std::printf("generated %ld lines\n", N());
        return 0;
    }
    long sum = 0;
    if (mode == "cin_sync") {                 // default: cin/cout synchronised with stdio
        Timer t{"cin >> (synced)"};
        long x; while (std::cin >> x) sum += x;
    } else if (mode == "cin_nosync") {
        std::ios::sync_with_stdio(false); std::cin.tie(nullptr);
        Timer t{"cin >> (no sync)"};
        long x; while (std::cin >> x) sum += x;
    } else if (mode == "scanf") {
        Timer t{"scanf"};
        long x; while (std::scanf("%ld", &x) == 1) sum += x;
    } else if (mode == "fread") {             // read everything at once, parse by hand
        Timer t{"fread + from_chars"};
        std::string all; char buf[1 << 16]; std::size_t n;
        while ((n = std::fread(buf, 1, sizeof buf, stdin)) > 0) all.append(buf, n);
        const char* p = all.data(); const char* end = p + all.size();
        while (p < end) {
            while (p < end && (*p == '\n' || *p == ' ')) ++p;
            long x; auto r = std::from_chars(p, end, x);
            if (r.ec != std::errc{}) break;
            sum += x; p = r.ptr;
        }
    } else if (mode == "parsers") {           // pure parsing cost, data already in memory
        std::vector<std::string> toks;
        for (long i = 0; i < N(); ++i) toks.push_back(std::to_string((i * 2654435761L) % 1000003));
        { Timer t{"istringstream"}; for (auto& s : toks) { std::istringstream is(s); long x; is >> x; sum += x; } }
        { Timer t{"stoi"}; for (auto& s : toks) sum += std::stoi(s); }
        { Timer t{"strtol"}; for (auto& s : toks) sum += std::strtol(s.c_str(), nullptr, 10); }
        { Timer t{"from_chars"}; for (auto& s : toks) { long x; std::from_chars(s.data(), s.data() + s.size(), x); sum += x; } }
    } else { std::fprintf(stderr, "usage: gen|cin_sync|cin_nosync|scanf|fread|parsers\n"); return 2; }
    std::printf("sum=%ld\n", sum);
}
