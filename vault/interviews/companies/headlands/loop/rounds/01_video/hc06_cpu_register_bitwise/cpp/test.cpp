// hc06 · CPU register bit operations — C++20 tests.  Same cases as test/RegisterSimTest.java plus C++-only edge cases
// (tag "cpp"): shift counts >= the width (UB in C++), huge rotate counts, strict from_chars parsing, bytes >= 0x80 in
// the input, 0 fed to the bit-counting functions, wrapping narrowing of the initial value, a corrupted opcode array.
#include <climits>
#include <iostream>
#include <random>
#include <type_traits>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace regsim;

namespace regsim {
template <class T> std::ostream& operator<<(std::ostream& os, const Masked<T>& m) { return os << "Masked(0x" << std::hex << m.mask << std::dec << ")"; }
template <class T> std::ostream& operator<<(std::ostream& os, const Counted<T>& c) { return os << "Counted(" << c.count << ")"; }
template <class T> std::ostream& operator<<(std::ostream& os, const BitOp<T>& b) { return os << "BitOp(" << b.bit << ")"; }
std::ostream& operator<<(std::ostream& os, const Run& r) {
    os << "Run{0x" << std::hex << r.reg << std::dec << ",[";
    for (int v : r.outputs) os << v << ";";
    return os << "]}";
}
}  // namespace regsim

namespace {

using Lines = std::vector<std::string>;

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

Reg ap(Reg reg, const Update& u) { return apply(reg, u); }

bool malformed(std::string_view text) {
    try { parse_line(text); } catch (const MalformedProgram&) { return true; } catch (...) { return false; }
    return false;
}

}  // namespace

// ================================================ Part 1: parse + execute

TEST(parses_every_base_mnemonic, "part1") {
    CHECK_EQ(parse_line("AND 0xFF"), Instr{And{0xFF}});
    CHECK_EQ(parse_line("and 255"), Instr{And{255}});
    CHECK_EQ(parse_line("  OR   0b1010 "), Instr{Or{0b1010}});
    CHECK_EQ(parse_line("Xor 0XF0"), Instr{Xor{0xF0}});
    CHECK_EQ(parse_line("NOT"), Instr{Not{}});
    CHECK_EQ(parse_line("SHL 3"), Instr{Shl(3)});
    CHECK_EQ(parse_line("SHR 4"), Instr{Shr(4)});
    CHECK_EQ(parse_line("ROL 5"), Instr{Rol(5)});
    CHECK_EQ(parse_line("ROR 6"), Instr{Ror(6)});
    CHECK_EQ(parse_line("SET 7"), Instr{SetBit(7)});
    CHECK_EQ(parse_line("CLEAR 8"), Instr{ClearBit(8)});
    CHECK_EQ(parse_line("TOGGLE 31"), Instr{ToggleBit(31)});
    CHECK_EQ(parse_line("POPCOUNT"), Instr{Popcount{}});
}

TEST(mask_operands_are_unsigned_32_bit, "part1,edge") {
    CHECK_EQ(parse_line("AND 0xFFFFFFFF"), Instr{And{0xFFFFFFFFu}});
    CHECK_EQ(parse_line("OR 2147483648"), Instr{Or{0x80000000u}});
    CHECK_EQ(parse_line("AND 4294967295"), Instr{And{0xFFFFFFFFu}});
}

TEST(rejects_malformed_lines, "part1,edge") {
    for (const char* bad : {"", "   ", "FOO", "AND", "AND 1 2", "NOT 3", "POPCOUNT 1", "SHL -1", "SHL 1.5", "SET 32", "SET -1", "CLEAR 99",
                            "TOGGLE 3x", "AND 0x1FFFFFFFF", "AND 4294967296", "AND -1", "AND xyz", "AND 0x", "AND 0b2", "SHL 99999999999"})
        CHECK(malformed(bad), std::string("should be malformed: '") + bad + "'");
}

TEST(types_guard_their_own_invariants, "part1,edge") {
    CHECK_THROWS_AS(SetBit(32), std::invalid_argument);
    CHECK_THROWS_AS(ClearBit(-1), std::invalid_argument);
    CHECK_THROWS_AS(ToggleBit(40), std::invalid_argument);
    CHECK_THROWS_AS(Shl(-1), std::invalid_argument);
    CHECK_THROWS_AS(Rol(-5), std::invalid_argument);
}

TEST(parse_program_skips_comments_and_blank_lines, "part1") {
    const auto prog = parse_program(lines("# a comment\n\nAND 0xFF\n   # indented comment\nNOT\n"));
    const std::vector<Instr> expected{Instr{And{255}}, Instr{Not{}}};
    CHECK_EQ(prog, expected);
    CHECK_EQ(parse_program({}).size(), 0);
}

TEST(bitwise_truth_tables, "part1") {
    CHECK_EQ(ap(0b1100, And{0b1010}), 0b1000u);
    CHECK_EQ(ap(0b1100, Or{0b1010}), 0b1110u);
    CHECK_EQ(ap(0b1100, Xor{0b1010}), 0b0110u);
    CHECK_EQ(ap(0, Not{}), 0xFFFFFFFFu);
    CHECK_EQ(ap(0x0000FFFF, Not{}), 0xFFFF0000u);
}

TEST(shifts_are_logical_and_drop_bits, "part1,edge") {
    CHECK_EQ(ap(0x80000000, Shl(1)), 0u);           // the top bit falls off
    CHECK_EQ(ap(0x80000000, Shr(31)), 1u);          // logical shift: zero fill, not sign fill
    CHECK_EQ(ap(0xF0000000, Shr(4)), 0x0F000000u);  // common mistake with a signed type: 0xFF000000
    CHECK_EQ(ap(0x30, Shl(4)), 0x300u);
    CHECK_EQ(ap(0x12345678, Shl(0)), 0x12345678u);
    CHECK_EQ(ap(0x12345678, Shr(0)), 0x12345678u);
}

TEST(shifts_of_32_or_more_clear_the_register, "part1,edge,cpp") {
    // In C++ `reg << 32` is undefined behaviour (not "== reg << 0" as in Java, not 0 as in hardware).  UBSan aborts on it.
    for (int n : {32, 33, 64, 1000, INT_MAX}) {
        CHECK_EQ(ap(0xFFFFFFFF, Shl(n)), 0u, "SHL " + std::to_string(n));
        CHECK_EQ(ap(0xFFFFFFFF, Shr(n)), 0u, "SHR " + std::to_string(n));
    }
    CHECK_EQ(ap(0xFFFFFFFF, Shl(31)), 0x80000000u);
    CHECK_EQ(ap(0xFFFFFFFF, Shr(31)), 1u);
}

TEST(rotations_wrap_around_and_take_modulo_32, "part1,edge") {
    CHECK_EQ(ap(0x12345678, Rol(4)), 0x23456781u);
    CHECK_EQ(ap(0x12345678, Ror(4)), 0x81234567u);
    CHECK_EQ(ap(0x12345678, Rol(32)), 0x12345678u);
    CHECK_EQ(ap(0x12345678, Ror(64)), 0x12345678u);
    CHECK_EQ(ap(0x12345678, Rol(36)), ap(0x12345678, Rol(4)));
    CHECK_EQ(ap(0x12345678, Rol(0)), 0x12345678u);
    CHECK_EQ(ap(0x80000000, Rol(1)), 1u);
    CHECK_EQ(ap(1, Ror(1)), 0x80000000u);
}

TEST(single_bit_operations_at_the_ends, "part1,edge") {
    CHECK_EQ(ap(0, SetBit(0)), 1u);
    CHECK_EQ(ap(0, SetBit(31)), 0x80000000u);
    CHECK_EQ(ap(0x80000000, SetBit(31)), 0x80000000u);  // idempotent
    CHECK_EQ(ap(0xFFFFFFFF, ClearBit(31)), 0x7FFFFFFFu);
    CHECK_EQ(ap(0xFFFFFFFF, ClearBit(0)), 0xFFFFFFFEu);
    CHECK_EQ(ap(0xFFFFFFFE, SetBit(0)), 0xFFFFFFFFu);
    CHECK_EQ(ap(0, ToggleBit(31)), 0x80000000u);
    CHECK_EQ(ap(0x80000000, ToggleBit(31)), 0u);
}

TEST(run_sample_program, "part1") {
    const auto prog = parse_program(lines("AND 0x3C\nSHL 4\nOR 0x0F\nPOPCOUNT\nNOT\nSHR 28\nPOPCOUNT\n"));
    const Run r = run(0xF0, prog);
    const std::vector<int> expected{6, 4};
    CHECK_EQ(r.outputs, expected);
    CHECK_EQ(r.reg, 0xFu);
    CHECK_EQ(unsigned_of(r.reg), 15u);
}

TEST(initial_value_range, "part1,edge") {
    CHECK_EQ(run(0xFFFF'FFFFll, {}).reg, 0xFFFFFFFFu);
    CHECK_EQ(unsigned_of(run(0xFFFF'FFFFll, {}).reg), 4'294'967'295ull);
    CHECK_EQ(run(0, {}).reg, 0u);
    CHECK_THROWS_AS(run(-1, {}), std::invalid_argument);
    CHECK_THROWS_AS(run(1ll << 32, {}), std::invalid_argument);
}

TEST(matches_a_64_bit_oracle, "part1,edge") {
    std::mt19937_64 rnd(0);
    for (int round = 0; round < 2000; ++round) {
        std::uint64_t oracle = rnd() & 0xFFFF'FFFFull;
        Reg reg = static_cast<Reg>(oracle);
        for (int step = 0; step < 20; ++step) {
            const int n = static_cast<int>(rnd() % 40);
            const std::uint64_t m = rnd() & 0xFFFF'FFFFull;
            switch (rnd() % 8) {
                case 0: reg = ap(reg, And{static_cast<Reg>(m)}); oracle &= m; break;
                case 1: reg = ap(reg, Or{static_cast<Reg>(m)}); oracle |= m; break;
                case 2: reg = ap(reg, Xor{static_cast<Reg>(m)}); oracle ^= m; break;
                case 3: reg = ap(reg, Not{}); oracle = ~oracle & 0xFFFF'FFFFull; break;
                case 4: reg = ap(reg, Shl(n)); oracle = n >= 32 ? 0 : (oracle << n) & 0xFFFF'FFFFull; break;
                case 5: reg = ap(reg, Shr(n)); oracle = n >= 32 ? 0 : oracle >> n; break;
                case 6: { reg = ap(reg, Rol(n)); const int k = n % 32; oracle = ((oracle << k) | (oracle >> (32 - k))) & 0xFFFF'FFFFull; break; }
                default: { reg = ap(reg, Ror(n)); const int k = n % 32; oracle = ((oracle >> k) | (oracle << (32 - k))) & 0xFFFF'FFFFull; break; }
            }
            CHECK_EQ(unsigned_of(reg), oracle, "round " + std::to_string(round) + " step " + std::to_string(step));
        }
    }
}

// ================================================ Part 2: unsigned semantics + formats

TEST(unsigned_interpretation, "part2") {
    CHECK_EQ(unsigned_of(0xFFFFFFFF), 4'294'967'295ull);
    CHECK_EQ(unsigned_of(0x80000000), 2'147'483'648ull);
    CHECK_EQ(unsigned_of(0), 0ull);
    CHECK_EQ(unsigned_of(0x7FFFFFFF), 2'147'483'647ull);
    CHECK_EQ(dec(0xFFFFFFFF), "4294967295");
    CHECK_EQ(dec(0x80000000), "2147483648");
    CHECK_EQ(dec(0), "0");
}

TEST(hex_is_eight_uppercase_digits, "part2,fmt") {
    CHECK_EQ(hex(0), "0x00000000");
    CHECK_EQ(hex(255), "0x000000FF");
    CHECK_EQ(hex(0xFFFFFFFF), "0xFFFFFFFF");
    CHECK_EQ(hex(0xDEADBEEF), "0xDEADBEEF");
    CHECK_EQ(hex(0x80000000), "0x80000000");
}

TEST(bin_is_thirty_two_digits_zero_padded, "part2,fmt") {
    CHECK_EQ(bin(0), "00000000000000000000000000000000");
    CHECK_EQ(bin(5), "00000000000000000000000000000101");
    CHECK_EQ(bin(0xFFFFFFFF), "11111111111111111111111111111111");
    CHECK_EQ(bin(0x80000000), "10000000000000000000000000000000");
}

TEST(describe_joins_three_views, "part2,fmt") {
    CHECK_EQ(describe(15), "0x0000000F 15 00000000000000000000000000001111");
    CHECK_EQ(describe(0xFFFFFFFF), "0xFFFFFFFF 4294967295 11111111111111111111111111111111");
}

TEST(parse_value_bases, "part2") {
    CHECK_EQ(parse_value("255"), 255u);
    CHECK_EQ(parse_value("0xFF"), 255u);
    CHECK_EQ(parse_value("0Xff"), 255u);
    CHECK_EQ(parse_value("0b101"), 5u);
    CHECK_EQ(parse_value("010"), 10u);  // decimal, not octal
    CHECK_EQ(parse_value("0"), 0u);
    CHECK_EQ(parse_value("0xFFFFFFFF"), 0xFFFFFFFFu);
    CHECK_EQ(parse_value("4294967295"), 0xFFFFFFFFu);
}

TEST(parse_value_rejects, "part2,edge") {
    for (const char* bad : {"", "-1", "+1", "0x", "0b", "0b2", "0xG", "4294967296", "0x100000000", "99999999999999999999", "1_000", "12 3"})
        CHECK_THROWS_AS(parse_value(bad), MalformedProgram, std::string("'") + bad + "'");
}

TEST(hex_round_trip, "part2") {
    std::mt19937 rnd(0);
    for (int i = 0; i < 1000; ++i) {
        const Reg x = rnd();
        CHECK_EQ(parse_value(hex(x)), x);
        CHECK_EQ(parse_value(dec(x)), x);
        CHECK_EQ(parse_value("0b" + bin(x)), x);
    }
}

TEST(solve_sample, "part2,fmt") {
    const Lines expected{"6", "4", "0x0000000F 15 00000000000000000000000000001111"};
    CHECK_EQ(solve(lines("0xF0\nAND 0x3C\nSHL 4\nOR 0x0F\nPOPCOUNT\nNOT\nSHR 28\nPOPCOUNT\n")), expected);
}

TEST(solve_with_no_instructions_and_with_the_high_bit, "part2,fmt") {
    const Lines zero{"0x00000000 0 00000000000000000000000000000000"};
    CHECK_EQ(solve({"0"}), zero);
    const Lines high{"0x80000000 2147483648 10000000000000000000000000000000"};
    CHECK_EQ(solve(lines("# initial\n0\n\nSET 31\n")), high);
    const Lines all{"0xFFFFFFFF 4294967295 11111111111111111111111111111111"};
    CHECK_EQ(solve({"4294967295"}), all);
}

TEST(solve_malformed, "part2,edge") {
    const Lines bad{"Malformed Input"};
    for (const char* text : {"", "# only a comment", "-5", "4294967296", "abc", "0\nFOO", "0\nAND", "0\nSET 32", "0\nSHL -1"})
        CHECK_EQ(solve(lines(text)), bad, std::string("'") + text + "'");
}

// ================================================ Part 3: extended instructions

TEST(parses_extended_mnemonics, "part3") {
    CHECK_EQ(parse_line("COMPRESS 0xF0"), Instr{Compress{0xF0}});
    CHECK_EQ(parse_line("expand 0xF0"), Instr{Expand{0xF0}});
    CHECK_EQ(parse_line("REVERSE"), Instr{Reverse{}});
    CHECK_EQ(parse_line("BSWAP"), Instr{ByteSwap{}});
    CHECK_EQ(parse_line("CTZ"), Instr{TrailingZeros{}});
    CHECK_EQ(parse_line("CLZ"), Instr{LeadingZeros{}});
    CHECK(malformed("REVERSE 1"));
    CHECK(malformed("COMPRESS"));
}

TEST(compress_and_expand_known_values, "part3") {
    CHECK_EQ(ap(0xB6, Compress{0xF0}), 0xBu);   // the high nibble
    CHECK_EQ(ap(0xB, Expand{0xF0}), 0xB0u);     // put it back at the mask positions
    CHECK_EQ(ap(0b10100100, Compress{0b10100100}), 0b111u);  // all mask positions hold 1 -> three adjacent ones
    CHECK_EQ(ap(0b10000100, Compress{0b10100100}), 0b101u);  // mask bits 2,5,7 hold 1,0,1 -> low first -> 101
    CHECK_EQ(ap(0xFFFFFFFF, Compress{0}), 0u);
    CHECK_EQ(ap(0xFFFFFFFF, Expand{0}), 0u);
    CHECK_EQ(ap(0x12345678, Compress{0xFFFFFFFF}), 0x12345678u);
    CHECK_EQ(ap(0x12345678, Expand{0xFFFFFFFF}), 0x12345678u);
}

TEST(compress_expand_match_a_loop_oracle_and_round_trip, "part3,edge") {
    std::mt19937 rnd(0);
    for (int i = 0; i < 5000; ++i) {
        const Reg x = rnd(), m = rnd();
        Reg expected = 0;
        int k = 0;
        for (int b = 0; b < 32; ++b)
            if ((m >> b) & 1u) expected |= ((x >> b) & 1u) << k++;
        CHECK_EQ(ap(x, Compress{m}), expected);
        CHECK_EQ(ap(ap(x, Compress{m}), Expand{m}), x & m, "expand(compress(x,m),m) == x & m");
    }
}

TEST(reverse_and_byte_swap, "part3") {
    CHECK_EQ(ap(1, Reverse{}), 0x80000000u);
    CHECK_EQ(ap(0, Reverse{}), 0u);
    CHECK_EQ(ap(0x0F, Reverse{}), 0xF0000000u);
    CHECK_EQ(ap(0x12345678, ByteSwap{}), 0x78563412u);
    std::mt19937 rnd(0);
    for (int i = 0; i < 100; ++i) {
        const Reg x = rnd();
        CHECK_EQ(ap(ap(x, Reverse{}), Reverse{}), x);
        CHECK_EQ(ap(ap(x, ByteSwap{}), ByteSwap{}), x);
    }
}

TEST(counting_queries, "part3,edge") {
    CHECK_EQ(query(0, TrailingZeros{}), 32);
    CHECK_EQ(query(8, TrailingZeros{}), 3);
    CHECK_EQ(query(0x80000000, TrailingZeros{}), 31);
    CHECK_EQ(query(1, TrailingZeros{}), 0);
    CHECK_EQ(query(0, LeadingZeros{}), 32);
    CHECK_EQ(query(1, LeadingZeros{}), 31);
    CHECK_EQ(query(0xFFFFFFFF, LeadingZeros{}), 0);
    CHECK_EQ(query(0xFFFFFFFF, Popcount{}), 32);
    CHECK_EQ(query(0, Popcount{}), 0);
    CHECK_EQ(query(0x80000000, Popcount{}), 1);
}

TEST(extended_program_end_to_end, "part3,fmt") {
    // 0x12345678 -BSWAP-> 0x78563412 (CTZ=1) -COMPRESS low nibbles-> 0x8642 -REVERSE-> 0x42610000 (CLZ=1)
    const Lines expected{"1", "1", "0x42610000 1113653248 01000010011000010000000000000000"};
    CHECK_EQ(solve(lines("0x12345678\nBSWAP\nCTZ\nCOMPRESS 0x0F0F0F0F\nREVERSE\nCLZ\n")), expected);
}

// ================================================ Part 4: decode once, vector<uint32_t> opcodes

namespace {

Instr random_instr(std::mt19937_64& rnd) {
    const int n = static_cast<int>(rnd() % 70), b = static_cast<int>(rnd() % 32);
    const Reg m = static_cast<Reg>(rnd());
    switch (rnd() % 18) {
        case 0: return And{m};
        case 1: return Or{m};
        case 2: return Xor{m};
        case 3: return Not{};
        case 4: return Shl(n);
        case 5: return Shr(n);
        case 6: return Rol(n);
        case 7: return Ror(n);
        case 8: return SetBit(b);
        case 9: return ClearBit(b);
        case 10: return ToggleBit(b);
        case 11: return Compress{m};
        case 12: return Expand{m};
        case 13: return Reverse{};
        case 14: return ByteSwap{};
        case 15: return Popcount{};
        case 16: return TrailingZeros{};
        default: return LeadingZeros{};
    }
}

std::vector<Instr> random_program(int n, std::uint64_t seed) {
    std::mt19937_64 rnd(seed);
    std::vector<Instr> prog;
    prog.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) prog.push_back(random_instr(rnd));
    return prog;
}

}  // namespace

TEST(compiled_agrees_with_interpreter_on_small_programs, "part4") {
    for (std::uint64_t seed = 0; seed < 300; ++seed) {
        const auto prog = random_program(60, seed);
        const long long init = static_cast<long long>(std::mt19937_64(seed)() & 0xFFFF'FFFFull);
        CHECK_EQ(execute(compile(prog), init), run(init, prog), "seed " + std::to_string(seed));
    }
}

TEST(compiled_edge_cases, "part4,edge") {
    const auto empty = compile({});
    CHECK_EQ(execute(empty, 0xFFFF'FFFFll), (Run{0xFFFFFFFFu, {}}));
    const std::vector<Instr> shifts{Shl(32), Popcount{}};
    CHECK_EQ(execute(compile(shifts), 0xFFFF'FFFFll), (Run{0u, {0}}));
    for (int n : {0, 1, 31, 32, 33, 63, 2'000'000'000, INT_MAX})
        for (const Instr& i : std::vector<Instr>{Shl(n), Shr(n), Rol(n), Ror(n)}) {
            const std::vector<Instr> p{i};
            CHECK_EQ(execute(compile(p), 0x89ABCDEFll), run(0x89ABCDEFll, p), "n=" + std::to_string(n));
        }
    CHECK_THROWS_AS(execute(empty, -1), std::invalid_argument);
    CHECK_THROWS_AS(execute(empty, 1ll << 32), std::invalid_argument);
}

TEST(compilation_folds_bit_ops_and_is_reusable, "part4") {
    const std::vector<Instr> prog{SetBit(4), ClearBit(0), ToggleBit(1), Not{}, Popcount{}};
    const Compiled c = compile(prog);
    CHECK_EQ(c.ops.size(), 5);
    CHECK_EQ(c.args.size(), 5);
    CHECK_EQ(c.query_count, 1);
    for (long long init : {0ll, 1ll, 0xFFFF'FFFFll, 0x1234'5678ll}) CHECK_EQ(execute(c, init), run(init, prog));
}

TEST(two_million_instructions, "part4,perf") {
    const auto prog = random_program(2'000'000, 0);
    const long long init = 0xDEADBEEFll;
    const Run expected = run(init, prog);
    CHECK_WITHIN_MS(2000, {
        const Compiled c = compile(prog);
        for (int pass = 0; pass < 20; ++pass) CHECK_EQ(execute(c, init), expected);
    });
    CHECK_WITHIN_MS(2000, CHECK_EQ(run(init, prog), expected););
}

// ================================================ C++-only edge cases (tag "cpp")

TEST(rotate_counts_of_any_size, "cpp,edge") {
    // std::rotl(x, s) is defined for every s >= 0 (it takes s mod 32); hand-written `(x << s) | (x >> (32 - s))` is UB at s == 0 and s >= 32.
    for (int n : {0, 32, 64, INT_MAX, INT_MAX - 1}) {
        CHECK_EQ(ap(0x89ABCDEF, Rol(n)), ap(0x89ABCDEF, Rol(n & 31)), "ROL " + std::to_string(n));
        CHECK_EQ(ap(0x89ABCDEF, Ror(n)), ap(0x89ABCDEF, Ror(n & 31)), "ROR " + std::to_string(n));
    }
}

TEST(bit_counting_of_zero_is_defined, "cpp,edge") {
    // __builtin_ctz(0) / __builtin_clz(0) are undefined; std::countr_zero(0u) == std::countl_zero(0u) == 32.
    const auto prog = parse_program({"CTZ", "CLZ", "POPCOUNT"});
    const std::vector<int> expected{32, 32, 0};
    CHECK_EQ(run(0, prog).outputs, expected);
    CHECK_EQ(execute(compile(prog), 0).outputs, expected);
}

TEST(from_chars_is_strict_and_must_consume_everything, "cpp,edge") {
    // std::from_chars: no '+', no leading whitespace, no "0x"; it succeeds on a valid PREFIX ("12abc" -> 12), so the end pointer decides.
    CHECK(malformed("AND 12abc"));
    CHECK(malformed("AND 0x1g"));
    CHECK(malformed("AND +1"));
    CHECK(malformed("SHL +1"));
    CHECK(malformed("SHL 1x"));
    CHECK(malformed("SET 3.0"));
    CHECK_EQ(parse_value(" 7 "), 7u);                 // surrounding whitespace is stripped
    CHECK_EQ(parse_value("0x000000000000000000000000000000FF"), 255u);  // 32 hex digits, leading zeros are fine
    CHECK_THROWS_AS(parse_value("0x" + std::string(41, '0')), MalformedProgram);  // over the 40-digit cap
    CHECK_EQ(parse_value("0b" + std::string(30, '0') + "11"), 3u);
}

TEST(bytes_above_127_and_nul_are_malformed_not_undefined, "cpp,edge") {
    // std::toupper / std::isspace with a negative char value is UB.  These must be plain "malformed".
    CHECK(malformed("\xC3\xA9ND 1"));
    CHECK(malformed("AND 0x\xFF"));
    CHECK(malformed("\xFF"));
    CHECK(malformed(std::string_view("AND 1\0 2", 8)));  // an embedded NUL is not whitespace and not a digit
    CHECK(malformed(std::string_view("AND\0 1", 6)));
    const Lines bad{"Malformed Input"};
    CHECK_EQ(solve({"\xFF"}), bad);
    CHECK_EQ(solve({"0", "\xC3\xA9"}), bad);
}

TEST(crlf_and_tab_separated_input, "cpp,fmt") {
    const Lines expected{"0x0000000F 15 00000000000000000000000000001111"};
    CHECK_EQ(solve({"0xF0\r", "SHR\t4\r", "\r", "# c\r"}), expected);
    CHECK_EQ(parse_line("\tshl\t3\r\n"), Instr{Shl(3)});
}

TEST(initial_value_does_not_wrap_when_narrowed, "cpp,edge") {
    // static_cast<uint32_t>(-1LL) == 0xFFFFFFFF: a missing range check would "accept" these as perfectly valid registers.
    for (long long bad : {-1ll, -4'294'967'295ll, 4'294'967'296ll, (1ll << 32) + 5, LLONG_MIN, LLONG_MAX}) {
        CHECK_THROWS_AS(run(bad, {}), std::invalid_argument);
        CHECK_THROWS_AS(execute(compile({}), bad), std::invalid_argument);
    }
    CHECK_EQ(run(4'294'967'295ll, {}).reg, 0xFFFFFFFFu);
}

TEST(instructions_are_small_trivially_copyable_values, "cpp") {
    static_assert(std::is_trivially_copyable_v<Instr>);
    static_assert(std::is_nothrow_move_constructible_v<Instr>);
    CHECK_LE(sizeof(Instr), 16u);
    CHECK_LE(sizeof(Update), 8u);
}

TEST(a_corrupted_opcode_array_is_an_error_not_a_wild_jump, "cpp,edge") {
    Compiled c;
    c.ops = {99u};
    c.args = {0};
    CHECK_THROWS_AS(execute(c, 0), std::logic_error);
}

TEST(unsigned_wrap_around_is_defined_but_signed_types_are_not_used, "cpp") {
    // 0 - 1 wraps to 0xFFFFFFFF for an unsigned register; the NOT of zero is the same value.
    const Reg zero = 0;
    CHECK_EQ(static_cast<Reg>(zero - 1), 0xFFFFFFFFu);
    CHECK_EQ(ap(0, Not{}), 0xFFFFFFFFu);
    CHECK_EQ(ap(0xFFFFFFFF, Xor{0xFFFFFFFF}), 0u);
    CHECK_EQ(ap(0x80000000, Rol(1)), 1u);
}

MT_MAIN()
