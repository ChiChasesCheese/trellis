// hc06 · CPU register bit operations — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
#pragma once

#include <bit>
#include <bitset>
#include <charconv>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>
#include <variant>
#include <vector>

namespace regsim {

/// The register: exactly 32 bits, unsigned.  Unsigned arithmetic wraps (defined); signed overflow and shifts by >= the
/// width are undefined behaviour in C++, so every shift count needs handling.
using Reg = std::uint32_t;

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

// ------------------------------------------------------------------------------------------------ Part 1: parse + execute
/// Decimal / 0x hex / 0b binary (prefix any case), range 0..0xFFFFFFFF, "010" is decimal 10; anything else -> MalformedProgram.
/// Hint: std::from_chars is strict (no '+', no whitespace, no 0x) but succeeds on a prefix: compare the end pointer.
inline Reg parse_value(std::string_view) { throw std::logic_error("TODO"); }

/// One line -> one instruction; mnemonic case-insensitive; wrong operand count / value -> MalformedProgram
/// (SetBit(32) and friends throw std::invalid_argument: translate it).  Avoid std::toupper on a plain char (negative = UB).
inline Instr parse_line(std::string_view) { throw std::logic_error("TODO"); }

/// Skips blank lines and lines starting with '#'.
inline std::vector<Instr> parse_program(const std::vector<std::string>&) { throw std::logic_error("TODO"); }

/// Execute one Update.  Shifts by >= 32 give 0 (`reg << 32` is UB in C++); SHR is logical; rotate counts are taken mod 32.
/// Hint: std::visit with an overloaded{...} set of lambdas, no default.  <bit> has rotl / rotr / popcount / countr_zero / countl_zero.
inline Reg apply(Reg, const Update&) { throw std::logic_error("TODO"); }

/// Execute one Query and return the number to print.
inline int query(Reg, const Query&) { throw std::logic_error("TODO"); }

/// The initial value must be in 0..0xFFFFFFFF, otherwise std::invalid_argument (do not static_cast first: -1 would wrap).
inline Run run(long long, const std::vector<Instr>&) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 2: unsigned semantics + formats
inline std::uint64_t unsigned_of(Reg) { throw std::logic_error("TODO"); }
/// Unsigned decimal.
inline std::string dec(Reg) { throw std::logic_error("TODO"); }
/// "0x" + 8 uppercase hex digits.
inline std::string hex(Reg) { throw std::logic_error("TODO"); }
/// 32 binary digits, zero padded.
inline std::string bin(Reg) { throw std::logic_error("TODO"); }
/// "hex dec bin", space separated.
inline std::string describe(Reg) { throw std::logic_error("TODO"); }
/// Whole problem: first non-blank non-comment line = initial value, the rest = program; one line per Query, then describe(final).
/// Anything malformed -> {"Malformed Input"}.
inline std::vector<std::string> solve(const std::vector<std::string>&) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 3
// COMPRESS / EXPAND (like Java Integer.compress / expand; C++20 has no standard function: write them), REVERSE, BSWAP
// (std::byteswap is C++23), CTZ, CLZ: add them to parse_line / apply / query.  std::countr_zero(0u) == 32.

// ------------------------------------------------------------------------------------------------ Part 4: decode once, vector<uint32_t> opcodes
/// A decoded program: two parallel arrays (opcode, operand) + the number of Queries.
/// NOT and SET / CLEAR / TOGGLE can be folded into XOR / OR / AND at decode time.
struct Compiled {
    std::vector<std::uint32_t> ops;
    std::vector<std::uint32_t> args;
    std::size_t query_count = 0;
};

/// Decode once.  Clamp shift counts to [0, 32]; rotate counts & 31.
inline Compiled compile(const std::vector<Instr>&) { throw std::logic_error("TODO"); }

/// Hot loop: array reads + one switch, no variant, no per-instruction allocation.  Result must equal run() exactly.
/// Hint: with the count clamped to <= 32, shift a uint64_t and truncate: no `if (count >= 32)` branch and no UB.
inline Run execute(const Compiled&, long long) { throw std::logic_error("TODO"); }

}  // namespace regsim
