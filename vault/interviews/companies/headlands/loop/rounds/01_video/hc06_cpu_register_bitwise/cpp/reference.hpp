// hc06 · CPU register bit operations — C++20 reference.  Statement: ../problem.md (Java: reference/RegisterSim.java).
// Parts: 1 parse + execute (std::variant instruction set, std::visit), 2 unsigned semantics + output formats + solve(),
//        3 extended instructions (compress/expand/reverse/bswap/ctz/clz), 4 compile once to a std::vector<uint32_t> opcode array.
#pragma once

#include <algorithm>
#include <bit>
#include <bitset>
#include <charconv>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>
#include <system_error>
#include <variant>
#include <vector>

namespace regsim {

/// The register: exactly 32 bits, unsigned.  Unsigned arithmetic wraps (defined); signed overflow and shifts by >= the
/// width are undefined behaviour, so the whole file uses Reg and handles every shift count explicitly.
using Reg = std::uint32_t;

namespace detail {
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
// Locale-free ASCII helpers.  std::isspace / std::toupper take an int that must be a valid unsigned char or EOF: passing a
// negative `char` (any byte >= 0x80 on signed-char platforms) is undefined behaviour.
constexpr bool is_space(char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\v' || c == '\f'; }
constexpr char to_upper(char c) { return c >= 'a' && c <= 'z' ? static_cast<char>(c - 'a' + 'A') : c; }
constexpr bool is_digit(char c) { return c >= '0' && c <= '9'; }
inline std::string_view strip(std::string_view s) {
    while (!s.empty() && is_space(s.front())) s.remove_prefix(1);
    while (!s.empty() && is_space(s.back())) s.remove_suffix(1);
    return s;
}
inline std::vector<std::string_view> split_words(std::string_view s) {
    std::vector<std::string_view> out;
    std::size_t i = 0;
    while (i < s.size()) {
        while (i < s.size() && is_space(s[i])) ++i;
        const std::size_t start = i;
        while (i < s.size() && !is_space(s[i])) ++i;
        if (i > start) out.push_back(s.substr(start, i - start));
    }
    return out;
}
}  // namespace detail

// ------------------------------------------------------------------------------------------------ instruction set
// Every instruction is a small value type; the closed set of them is a std::variant.  Update changes the register,
// Query only reads it and produces a number to print: "does it modify the register" is a fact of the type.
template <class Tag> struct Masked {
    Reg mask;
    friend bool operator==(const Masked&, const Masked&) = default;
};
template <class Tag> struct Counted {  // shift / rotate count, >= 0
    int count;
    explicit Counted(int c) : count(c) {
        if (c < 0) throw std::invalid_argument("count < 0: " + std::to_string(c));
    }
    friend bool operator==(const Counted&, const Counted&) = default;
};
template <class Tag> struct BitOp {  // bit number 0..31
    int bit;
    explicit BitOp(int b) : bit(b) {
        if (b < 0 || b > 31) throw std::invalid_argument("bit out of 0..31: " + std::to_string(b));
    }
    friend bool operator==(const BitOp&, const BitOp&) = default;
};

using And = Masked<struct AndTag>;
using Or = Masked<struct OrTag>;
using Xor = Masked<struct XorTag>;
struct Not { friend bool operator==(const Not&, const Not&) = default; };
using Shl = Counted<struct ShlTag>;
using Shr = Counted<struct ShrTag>;
using Rol = Counted<struct RolTag>;
using Ror = Counted<struct RorTag>;
using SetBit = BitOp<struct SetTag>;
using ClearBit = BitOp<struct ClearTag>;
using ToggleBit = BitOp<struct ToggleTag>;
struct Popcount { friend bool operator==(const Popcount&, const Popcount&) = default; };
// Part 3
using Compress = Masked<struct CompressTag>;
using Expand = Masked<struct ExpandTag>;
struct Reverse { friend bool operator==(const Reverse&, const Reverse&) = default; };
struct ByteSwap { friend bool operator==(const ByteSwap&, const ByteSwap&) = default; };
struct TrailingZeros { friend bool operator==(const TrailingZeros&, const TrailingZeros&) = default; };
struct LeadingZeros { friend bool operator==(const LeadingZeros&, const LeadingZeros&) = default; };

using Update = std::variant<And, Or, Xor, Not, Shl, Shr, Rol, Ror, SetBit, ClearBit, ToggleBit, Compress, Expand, Reverse, ByteSwap>;
using Query = std::variant<Popcount, TrailingZeros, LeadingZeros>;
using Instr = std::variant<Update, Query>;

struct MalformedProgram : std::runtime_error {
    using std::runtime_error::runtime_error;
};

/// Final register + the output of every Query, in program order.
struct Run {
    Reg reg;
    std::vector<int> outputs;
    friend bool operator==(const Run&, const Run&) = default;
};

// ------------------------------------------------------------------------------------------------ Part 1: parse
/// Decimal / 0x hex / 0b binary (prefix any case), range 0..0xFFFFFFFF, "010" is decimal 10.
/// std::from_chars is the strict tool: no leading whitespace, no '+', no 0x prefix, no locale.  It stops at the first bad
/// character and still reports success, so the end pointer must be checked: "12abc" parses as 12 otherwise.
inline Reg parse_value(std::string_view token) {
    const std::string shown(token);
    token = detail::strip(token);
    int radix = 10;
    std::string_view digits = token;
    if (token.size() > 2 && token[0] == '0') {
        const char p = detail::to_upper(token[1]);
        if (p == 'X') { radix = 16; digits = token.substr(2); }
        else if (p == 'B') { radix = 2; digits = token.substr(2); }
    }
    if (digits.empty() || digits.size() > 40) throw MalformedProgram("bad number: '" + shown + "'");
    std::uint64_t v = 0;  // 64 bits: 0xFFFFFFFF + 1 must be detectable, not wrap
    const auto [end, ec] = std::from_chars(digits.data(), digits.data() + digits.size(), v, radix);
    if (ec == std::errc::result_out_of_range) throw MalformedProgram("number too large: '" + shown + "'");
    if (ec != std::errc{} || end != digits.data() + digits.size()) throw MalformedProgram("bad number: '" + shown + "'");
    if (v > 0xFFFF'FFFFull) throw MalformedProgram("number exceeds 32 bits: '" + shown + "'");
    return static_cast<Reg>(v);
}

namespace detail {
inline const std::string_view& operand(const std::vector<std::string_view>& w) {
    if (w.size() != 2) throw MalformedProgram(std::string(w[0]) + " takes exactly one operand");
    return w[1];
}
inline Reg mask_arg(const std::vector<std::string_view>& w) { return parse_value(operand(w)); }
inline int small_arg(const std::vector<std::string_view>& w) {
    const std::string_view s = operand(w);
    for (char c : s)
        if (!is_digit(c)) throw MalformedProgram("bad count: '" + std::string(s) + "'");
    int v = 0;
    const auto [end, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    if (ec != std::errc{} || end != s.data() + s.size()) throw MalformedProgram("count too large: '" + std::string(s) + "'");
    return v;
}
template <class T> Instr bare(const std::vector<std::string_view>& w, T instr) {
    if (w.size() != 1) throw MalformedProgram(std::string(w[0]) + " takes no operand");
    return instr;
}
}  // namespace detail

/// One line -> one instruction; the mnemonic is case-insensitive; any problem throws MalformedProgram.
/// The instruction types guard their own invariants with std::invalid_argument (SetBit(32)); the parse boundary translates
/// that into the one error the caller handles.  MalformedProgram is a runtime_error, so it is not caught by mistake.
inline Instr parse_line(std::string_view line) {
    const auto w = detail::split_words(line);
    if (w.empty()) throw MalformedProgram("empty line");
    std::string m(w[0]);
    for (char& c : m) c = detail::to_upper(c);
    try {
        if (m == "AND") return And{detail::mask_arg(w)};
        if (m == "OR") return Or{detail::mask_arg(w)};
        if (m == "XOR") return Xor{detail::mask_arg(w)};
        if (m == "NOT") return detail::bare(w, Not{});
        if (m == "SHL") return Shl(detail::small_arg(w));
        if (m == "SHR") return Shr(detail::small_arg(w));
        if (m == "ROL") return Rol(detail::small_arg(w));
        if (m == "ROR") return Ror(detail::small_arg(w));
        if (m == "SET") return SetBit(detail::small_arg(w));
        if (m == "CLEAR") return ClearBit(detail::small_arg(w));
        if (m == "TOGGLE") return ToggleBit(detail::small_arg(w));
        if (m == "POPCOUNT") return detail::bare(w, Popcount{});
        if (m == "COMPRESS") return Compress{detail::mask_arg(w)};
        if (m == "EXPAND") return Expand{detail::mask_arg(w)};
        if (m == "REVERSE") return detail::bare(w, Reverse{});
        if (m == "BSWAP") return detail::bare(w, ByteSwap{});
        if (m == "CTZ") return detail::bare(w, TrailingZeros{});
        if (m == "CLZ") return detail::bare(w, LeadingZeros{});
    } catch (const std::invalid_argument& e) {
        throw MalformedProgram(e.what());
    }
    throw MalformedProgram("unknown instruction: " + std::string(w[0]));
}

/// Skips blank lines and lines starting with '#'.
inline std::vector<Instr> parse_program(const std::vector<std::string>& lines) {
    std::vector<Instr> out;
    for (const std::string& line : lines) {
        const std::string_view s = detail::strip(line);
        if (s.empty() || s.front() == '#') continue;
        out.push_back(parse_line(s));
    }
    return out;
}

// ------------------------------------------------------------------------------------------------ bit helpers
namespace detail {
/// Gather the bits of x selected by mask into the low bits (Java Integer.compress, x86 PEXT).  Loop over the set bits of the mask only.
inline Reg compress_bits(Reg x, Reg m) {
    Reg out = 0;
    int k = 0;
    for (; m != 0; m &= m - 1) {  // m & (m - 1) clears the lowest set bit
        const int b = std::countr_zero(m);
        out |= ((x >> b) & 1u) << k++;
    }
    return out;
}
/// Scatter the low bits of x to the positions of the mask's set bits (Integer.expand, PDEP).
inline Reg expand_bits(Reg x, Reg m) {
    Reg out = 0;
    int k = 0;
    for (; m != 0; m &= m - 1) {
        const int b = std::countr_zero(m);
        out |= ((x >> k++) & 1u) << b;
    }
    return out;
}
inline Reg byte_swap(Reg v) { return (v >> 24) | ((v >> 8) & 0x0000FF00u) | ((v << 8) & 0x00FF0000u) | (v << 24); }  // std::byteswap is C++23
inline Reg bit_reverse(Reg v) {  // swap adjacent bits, then pairs, then nibbles, then reverse the bytes
    v = ((v >> 1) & 0x55555555u) | ((v & 0x55555555u) << 1);
    v = ((v >> 2) & 0x33333333u) | ((v & 0x33333333u) << 2);
    v = ((v >> 4) & 0x0F0F0F0Fu) | ((v & 0x0F0F0F0Fu) << 4);
    return byte_swap(v);
}
}  // namespace detail

/// Execute one Update.  Shifts by >= 32 give 0 explicitly (`reg << 32` is undefined behaviour in C++; the hardware gives 0 here);
/// SHR on an unsigned type is a logical shift; rotate counts are taken mod 32 by std::rotl / std::rotr for any count >= 0.
/// There is no default: the overload set must cover all 15 alternatives or this does not compile.
inline Reg apply(Reg reg, const Update& u) {
    return std::visit(
        detail::overloaded{
            [&](const And& i) -> Reg { return reg & i.mask; },
            [&](const Or& i) -> Reg { return reg | i.mask; },
            [&](const Xor& i) -> Reg { return reg ^ i.mask; },
            [&](const Not&) -> Reg { return ~reg; },
            [&](const Shl& i) -> Reg { return i.count >= 32 ? Reg{0} : reg << i.count; },
            [&](const Shr& i) -> Reg { return i.count >= 32 ? Reg{0} : reg >> i.count; },
            [&](const Rol& i) -> Reg { return std::rotl(reg, i.count); },
            [&](const Ror& i) -> Reg { return std::rotr(reg, i.count); },
            [&](const SetBit& i) -> Reg { return reg | (Reg{1} << i.bit); },
            [&](const ClearBit& i) -> Reg { return reg & ~(Reg{1} << i.bit); },
            [&](const ToggleBit& i) -> Reg { return reg ^ (Reg{1} << i.bit); },
            [&](const Compress& i) -> Reg { return detail::compress_bits(reg, i.mask); },
            [&](const Expand& i) -> Reg { return detail::expand_bits(reg, i.mask); },
            [&](const Reverse&) -> Reg { return detail::bit_reverse(reg); },
            [&](const ByteSwap&) -> Reg { return detail::byte_swap(reg); }},
        u);
}

/// Execute one Query.  std::popcount / countr_zero / countl_zero are defined for 0 (0 / 32 / 32); __builtin_ctz(0) is undefined.
inline int query(Reg reg, const Query& q) {
    return std::visit(detail::overloaded{[&](const Popcount&) { return std::popcount(reg); },
                                         [&](const TrailingZeros&) { return std::countr_zero(reg); },
                                         [&](const LeadingZeros&) { return std::countl_zero(reg); }},
                      q);
}

namespace detail {
/// The initial value arrives as long long: 4294967295 does not fit a *signed* 32-bit type, and static_cast<Reg>(-1LL)
/// would silently wrap, so the range is checked before narrowing.
inline Reg checked_initial(long long initial) {
    if (initial < 0 || initial > 0xFFFF'FFFFll) throw std::invalid_argument("initial out of 0..2^32-1: " + std::to_string(initial));
    return static_cast<Reg>(initial);
}
}  // namespace detail

inline Run run(long long initial, const std::vector<Instr>& program) {
    Reg reg = detail::checked_initial(initial);
    std::vector<int> out;
    for (const Instr& i : program)
        std::visit(detail::overloaded{[&](const Update& u) { reg = apply(reg, u); },
                                      [&](const Query& q) { out.push_back(query(reg, q)); }},
                   i);
    return {reg, std::move(out)};
}

// ------------------------------------------------------------------------------------------------ Part 2
inline std::uint64_t unsigned_of(Reg reg) { return reg; }

/// Unsigned decimal.
inline std::string dec(Reg reg) { return std::to_string(reg); }

/// "0x" + 8 uppercase hex digits.
inline std::string hex(Reg reg) {
    static constexpr char digits[] = "0123456789ABCDEF";
    std::string s = "0x00000000";
    for (int i = 0; i < 8; ++i) s[static_cast<std::size_t>(9 - i)] = digits[(reg >> (4 * i)) & 0xFu];
    return s;
}

/// 32 binary digits, zero padded (std::bitset prints every bit).
inline std::string bin(Reg reg) { return std::bitset<32>(reg).to_string(); }

inline std::string describe(Reg reg) { return hex(reg) + " " + dec(reg) + " " + bin(reg); }

/// Whole problem: first non-blank non-comment line is the initial value, the rest is the program; one output line per Query,
/// then describe(final).  Anything malformed -> {"Malformed Input"}.
inline std::vector<std::string> solve(const std::vector<std::string>& lines) {
    try {
        std::vector<std::string> body;
        for (const std::string& l : lines) {
            const std::string_view s = detail::strip(l);
            if (!s.empty() && s.front() != '#') body.push_back(l);
        }
        if (body.empty()) throw MalformedProgram("missing initial value");
        const Reg initial = parse_value(body.front());
        const Run r = run(initial, parse_program(std::vector<std::string>(body.begin() + 1, body.end())));
        std::vector<std::string> out;
        for (int v : r.outputs) out.push_back(std::to_string(v));
        out.push_back(describe(r.reg));
        return out;
    } catch (const MalformedProgram&) {
        return {"Malformed Input"};
    }
}

// ------------------------------------------------------------------------------------------------ Part 4
namespace detail {
enum : std::uint32_t { OP_AND, OP_OR, OP_XOR, OP_SHL, OP_SHR, OP_ROL, OP_ROR, OP_COMPRESS, OP_EXPAND, OP_REVERSE, OP_BSWAP, OP_POPCOUNT, OP_CTZ, OP_CLZ };
}

/// A decoded program: two parallel arrays of uint32_t (opcode, operand) plus the number of Queries.
/// NOT and SET / CLEAR / TOGGLE are folded into XOR / OR / AND at decode time.  Contiguous integers prefetch well; a vector of
/// std::variant would pay a discriminator check and a larger, padded element for every instruction.
struct Compiled {
    std::vector<std::uint32_t> ops;
    std::vector<std::uint32_t> args;
    std::size_t query_count = 0;
};

inline Compiled compile(const std::vector<Instr>& program) {
    using namespace detail;
    Compiled c;
    c.ops.reserve(program.size());
    c.args.reserve(program.size());
    auto emit = [&](std::uint32_t op, std::uint32_t arg) { c.ops.push_back(op); c.args.push_back(arg); };
    const auto on_update = overloaded{
        [&](const And& i) { emit(OP_AND, i.mask); },
        [&](const Or& i) { emit(OP_OR, i.mask); },
        [&](const Xor& i) { emit(OP_XOR, i.mask); },
        [&](const Not&) { emit(OP_XOR, 0xFFFF'FFFFu); },
        [&](const Shl& i) { emit(OP_SHL, static_cast<std::uint32_t>(std::min(i.count, 32))); },  // clamp: any count >= 32 means "all bits out"
        [&](const Shr& i) { emit(OP_SHR, static_cast<std::uint32_t>(std::min(i.count, 32))); },
        [&](const Rol& i) { emit(OP_ROL, static_cast<std::uint32_t>(i.count & 31)); },
        [&](const Ror& i) { emit(OP_ROR, static_cast<std::uint32_t>(i.count & 31)); },
        [&](const SetBit& i) { emit(OP_OR, Reg{1} << i.bit); },
        [&](const ClearBit& i) { emit(OP_AND, ~(Reg{1} << i.bit)); },
        [&](const ToggleBit& i) { emit(OP_XOR, Reg{1} << i.bit); },
        [&](const Compress& i) { emit(OP_COMPRESS, i.mask); },
        [&](const Expand& i) { emit(OP_EXPAND, i.mask); },
        [&](const Reverse&) { emit(OP_REVERSE, 0); },
        [&](const ByteSwap&) { emit(OP_BSWAP, 0); }};
    const auto on_query = overloaded{
        [&](const Popcount&) { emit(OP_POPCOUNT, 0); ++c.query_count; },
        [&](const TrailingZeros&) { emit(OP_CTZ, 0); ++c.query_count; },
        [&](const LeadingZeros&) { emit(OP_CLZ, 0); ++c.query_count; }};
    for (const Instr& i : program)
        std::visit(overloaded{[&](const Update& u) { std::visit(on_update, u); }, [&](const Query& q) { std::visit(on_query, q); }}, i);
    return c;
}

/// Hot loop: array reads, one switch, no variant, no allocation besides the output vector.
/// Shifts are done in 64 bits: the count was clamped to [0, 32], and a 64-bit shift by <= 32 is defined and drops cleanly
/// into 0 after truncation, so there is no `if (count >= 32)` branch.
/// The switch is one indirect jump; with random opcodes the branch predictor misses it often: that, not the arithmetic, is the cost.
inline Run execute(const Compiled& c, long long initial) {
    using namespace detail;
    Reg reg = checked_initial(initial);
    std::vector<int> out;
    out.reserve(c.query_count);
    const std::uint32_t* ops = c.ops.data();
    const std::uint32_t* args = c.args.data();
    const std::size_t n = c.ops.size();
    for (std::size_t pc = 0; pc < n; ++pc) {
        const std::uint32_t a = args[pc];
        switch (ops[pc]) {
            case OP_AND: reg &= a; break;
            case OP_OR: reg |= a; break;
            case OP_XOR: reg ^= a; break;
            case OP_SHL: reg = static_cast<Reg>(static_cast<std::uint64_t>(reg) << a); break;
            case OP_SHR: reg = static_cast<Reg>(static_cast<std::uint64_t>(reg) >> a); break;
            case OP_ROL: reg = std::rotl(reg, static_cast<int>(a)); break;
            case OP_ROR: reg = std::rotr(reg, static_cast<int>(a)); break;
            case OP_COMPRESS: reg = compress_bits(reg, a); break;
            case OP_EXPAND: reg = expand_bits(reg, a); break;
            case OP_REVERSE: reg = bit_reverse(reg); break;
            case OP_BSWAP: reg = byte_swap(reg); break;
            case OP_POPCOUNT: out.push_back(std::popcount(reg)); break;
            case OP_CTZ: out.push_back(std::countr_zero(reg)); break;
            case OP_CLZ: out.push_back(std::countl_zero(reg)); break;
            default: throw std::logic_error("bad opcode " + std::to_string(ops[pc]));
        }
    }
    return {reg, std::move(out)};
}

}  // namespace regsim
