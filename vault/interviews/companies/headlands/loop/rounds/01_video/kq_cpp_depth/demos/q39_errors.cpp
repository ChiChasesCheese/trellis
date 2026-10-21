// Error handling cost: return codes, exceptions, std::optional / std::expected.
#include <chrono>
#include <cstdio>
#include <optional>
#include <stdexcept>
#include <string>

template <class F> double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now(); f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

__attribute__((noinline)) int parse_code(int x, int& out) { if (x % 100 == 0) return -1; out = x; return 0; }
__attribute__((noinline)) int parse_throw(int x) { if (x % 100 == 0) throw std::invalid_argument("bad"); return x; }
__attribute__((noinline)) std::optional<int> parse_opt(int x) { if (x % 100 == 0) return std::nullopt; return x; }

int main() {
    const int N = 1'000'000;
    long s1 = 0, s2 = 0, s3 = 0, e1 = 0, e2 = 0, e3 = 0;
    double t_code = ms([&] { for (int i = 1; i <= N; ++i) { int v; if (parse_code(i, v) == 0) s1 += v; else ++e1; } });
    double t_opt  = ms([&] { for (int i = 1; i <= N; ++i) { if (auto v = parse_opt(i)) s3 += *v; else ++e3; } });
    double t_exc  = ms([&] { for (int i = 1; i <= N; ++i) { try { s2 += parse_throw(i); } catch (const std::exception&) { ++e2; } } });
    std::printf("1M calls, 1%% fail: return code %.1f ms | optional %.1f ms | exceptions %.1f ms\n", t_code, t_opt, t_exc);
    std::printf("failures seen: %ld %ld %ld\n", e1, e3, e2);

    long e4 = 0;
    double t_ok = ms([&] { for (int i = 1; i <= N; ++i) { try { s2 += parse_throw(i + 1 - (i % 100 == 99)); } catch (...) { ++e4; } } });
    std::printf("1M calls, almost never failing, exceptions: %.1f ms (failures %ld) - the no-throw path is nearly free\n", t_ok, e4);
    return (s1 + s2 + s3) == 0;
}
