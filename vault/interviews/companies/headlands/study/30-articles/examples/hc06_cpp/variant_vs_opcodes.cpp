// Same random program, two representations: vector<variant> + std::visit  vs  two vector<uint32_t> + one switch.
#include <bit>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <random>
#include <variant>
#include <vector>

struct And { std::uint32_t m; };
struct Or { std::uint32_t m; };
struct Xor { std::uint32_t m; };
struct Rol { int n; };
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

int main() {
    constexpr int N = 4'000'000;
    std::mt19937 rng(1);
    using Instr = std::variant<And, Or, Xor, Rol>;
    std::vector<Instr> prog;
    std::vector<std::uint32_t> ops, args;
    for (int i = 0; i < N; ++i) {
        const std::uint32_t m = rng(), kind = rng() % 4;
        switch (kind) {
            case 0: prog.push_back(And{m}); break;
            case 1: prog.push_back(Or{m}); break;
            case 2: prog.push_back(Xor{m}); break;
            default: prog.push_back(Rol{static_cast<int>(m % 70)}); break;
        }
        ops.push_back(kind);
        args.push_back(kind == 3 ? m % 70 : m);
    }
    using clock = std::chrono::steady_clock;
    auto ms = [](auto d) { return std::chrono::duration<double, std::milli>(d).count(); };

    auto t0 = clock::now();
    std::uint32_t a = 0xDEADBEEF;
    for (int pass = 0; pass < 5; ++pass)
        for (const Instr& i : prog)
            a = std::visit(overloaded{[&](const And& x) { return a & x.m; }, [&](const Or& x) { return a | x.m; },
                                      [&](const Xor& x) { return a ^ x.m; }, [&](const Rol& x) { return std::rotl(a, x.n); }}, i);
    auto t1 = clock::now();

    std::uint32_t b = 0xDEADBEEF;
    for (int pass = 0; pass < 5; ++pass)
        for (std::size_t pc = 0; pc < ops.size(); ++pc) {
            switch (ops[pc]) {
                case 0: b &= args[pc]; break;
                case 1: b |= args[pc]; break;
                case 2: b ^= args[pc]; break;
                default: b = std::rotl(b, static_cast<int>(args[pc])); break;
            }
        }
    auto t2 = clock::now();
    std::cout << "same result: " << std::boolalpha << (a == b) << "  sizeof(Instr)=" << sizeof(Instr) << " (opcode + operand = 8 bytes in the arrays too)\n"
              << "variant + visit: " << ms(t1 - t0) << " ms,  opcode arrays: " << ms(t2 - t1) << " ms  (build with -O2)\n";
}
