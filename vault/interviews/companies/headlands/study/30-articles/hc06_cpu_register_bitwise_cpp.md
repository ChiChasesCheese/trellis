# hc06 · CPU 寄存器位运算（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

一个 CPU 寄存器就是 32 个开关（bit）。给你初值和一串指令，依次执行，输出指令要求的计数，最后输出寄存器终值的三种视图。

```
0xF0          ← 第 1 个有效行：初值（十进制 / 0x 十六进制 / 0b 二进制），范围 0..4294967295
AND 0x3C      ← 其余每行一条指令，助记符不分大小写；空行与 # 开头的行忽略
SHL 4
OR 0x0F
POPCOUNT
NOT
SHR 28
POPCOUNT
```

| 指令 | 语义（`r` = 当前寄存器） | Part |
|---|---|---|
| `AND m` · `OR m` · `XOR m` | `r op m`（m 是 0..2³²−1 的无符号数） | 1 |
| `NOT` | 所有位取反 | 1 |
| `SHL n` · `SHR n` | 逻辑左移 / 右移（补 0）；**n ≥ 32 → 结果 0** | 1 |
| `ROL n` · `ROR n` | 循环左移 / 右移；位数 mod 32 | 1 |
| `SET b` · `CLEAR b` · `TOGGLE b` | 第 b 位（0 = 最低位）置 1 / 清 0 / 翻转；b ∈ 0..31 | 1 |
| `POPCOUNT` | **输出** r 里 1 的个数（不改 r） | 1 |
| `COMPRESS m` · `EXPAND m` | 把 m 为 1 的那些位收拢到低位 / 散开到 m 为 1 的位置 | 3 |
| `REVERSE` · `BSWAP` | 32 位整体翻转 / 字节序翻转 | 3 |
| `CTZ` · `CLZ` | **输出** 末尾 0 的个数 / 前导 0 的个数（r = 0 时都是 32） | 3 |

| Part | 内容 |
|---|---|
| 1 | 解析成指令类型，用 `std::visit` 执行 |
| 2 | 无符号语义、输出格式（`0x` + 8 位大写十六进制，无符号十进制，32 位二进制）、整题 `solve` |
| 3 | 扩展指令 |
| 4 | 解码一次到 `std::vector<uint32_t>` 操作码数组，热循环不分配、移位无分支；结果必须和 Part 1 的解释器完全相同 |

输入有任何问题（格式、范围、未知指令、位号越界）→ 只输出 `Malformed Input`。每条输出型指令（POPCOUNT / CTZ / CLZ）输出一行十进制，最后一行是终值：

```
6
4
0x0000000F 15 00000000000000000000000000001111
```

手算：`0xF0 AND 0x3C = 0x30`；`SHL 4` → `0x300`；`OR 0x0F` → `0x30F`，`POPCOUNT` = 2 + 4 = **6**；`NOT` → `0xFFFFFCF0`；`SHR 28` → `0xF`，`POPCOUNT` = **4**；终值 `0xF` = 十进制 15。

## 2. 地基：为什么寄存器用 `std::uint32_t`

整题的难点是「32 个二进制位在语言里怎么存」。

* **补码（two's complement）**：`int` 把最高位当符号位，`0xFFFFFFFF` 作为 `int` 是 −1。32 个 bit 完全一样，只是**怎么解释**不同。
* **逻辑右移 vs 算术右移**：无符号类型右移补 0（逻辑，logical）；有符号类型右移补符号位（算术，arithmetic），`0xF0000000 >> 4` 得到 `0xFF000000`。这里要逻辑移位。
* **UB（未定义行为）清单**，位运算题的每一条都是潜在的 bug：

| 写法 | 结果 |
|---|---|
| 有符号整数溢出（`INT_MAX + 1`） | UB |
| 移位位数 ≥ 类型宽度（`x << 32`，`uint32_t`） | **UB**（Java 是 mod 32；硬件是 0） |
| 移位位数为负 | UB |
| 无符号加减乘溢出 | 定义良好，按 2^32 回绕 |
| `__builtin_ctz(0)` / `__builtin_clz(0)` | UB |
| `std::countr_zero(0u)` / `std::countl_zero(0u)` | 定义良好，都是 32 |
| `std::toupper(c)` / `std::isspace(c)` 传负数 `char` | UB（字节 ≥ 0x80 时） |

所以：**寄存器用 `std::uint32_t`**（一个确定 32 位的无符号类型，回绕有定义，右移是逻辑的），**每个移位位数都显式处理**，**字符分类自己写 ASCII 版**。

下面是文件开头：

```cpp
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
```

## 3. 指令集：一个封闭的 `std::variant`

每条指令是一个小的值类型，全体指令的集合是 `std::variant`。分成两层：

* `Update`：改寄存器的 15 种；
* `Query`：只读寄存器、产生一个要输出的数的 3 种；
* `Instr = std::variant<Update, Query>`。

「会不会改寄存器」是类型层面的事实：`apply` 只接受 `Update`，返回新寄存器值；`Query` 的返回值含义不同，混在一起返回类型会含糊。

```cpp
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
```

要点：

* 带操作数的指令用三个小模板（`Masked`：掩码；`Counted`：移位 / 旋转位数；`BitOp`：位号）。`Tag` 只是让 `And` 和 `Or` 成为**不同的类型**。
* `Counted`、`BitOp` 的构造函数守住不变量（位数 ≥ 0，位号 0..31），违反就抛 `std::invalid_argument`；`explicit` 防止 `Shl s = 3;` 这种隐式转换。
* `operator==` 全部 `= default`：测试和 `Run` 的比较不用手写。
* 可以直接写 `Instr i = And{0xFF};` ——`std::variant` 的转换构造函数会挑出唯一能装下它的备选项（`Update` 里的 `And`）。
* `MalformedProgram` 继承 `std::runtime_error`，**不**继承 `invalid_argument`：解析边界要把前者当成「输入格式错误」，把类型构造函数抛的 `invalid_argument` 翻译成它，不能混。

## 4. Part 1：解析

### 4.1 数字：`std::from_chars` 又严格又有陷阱

要求：十进制 / `0x` / `0b`（前缀不分大小写）；范围 0..0xFFFFFFFF；`010` 是十进制 10，**不是八进制**；`+1`、`-1`、`1_000`、`0x`（只有前缀）都是格式错误。

`std::from_chars` 不看区域设置、不跳空白、不认 `+`、不认 `0x`——正是这里要的严格。但它有一个经典陷阱：**成功解析一个合法前缀就算成功**。

```cpp
// std::from_chars: strict (no '+', no spaces, no 0x, no locale), but it succeeds on a valid PREFIX.
#include <charconv>
#include <cstdint>
#include <iostream>
#include <string_view>

void try_parse(std::string_view s, int base = 10) {
    std::uint64_t v = 0;
    const auto [end, ec] = std::from_chars(s.data(), s.data() + s.size(), v, base);
    const bool consumed_all = end == s.data() + s.size();
    std::cout << "'" << s << "' base " << base << ": ec=" << (ec == std::errc{} ? "ok" : ec == std::errc::result_out_of_range ? "out_of_range" : "invalid")
              << ", value=" << v << ", consumed all: " << std::boolalpha << consumed_all << "\n";
}

int main() {
    try_parse("12abc");        // ok, value 12, consumed all: false  <- the end pointer decides
    try_parse("+1");           // invalid: no plus sign
    try_parse("-1");           // invalid for an unsigned target
    try_parse("0xFF", 16);     // ok, value 0, stops at 'x': the prefix must be stripped by hand
    try_parse("FF", 16);       // ok
    try_parse("18446744073709551616");  // 2^64: out_of_range
}
```

```text
'12abc' base 10: ec=ok, value=12, consumed all: false
'+1' base 10: ec=invalid, value=0, consumed all: false
'-1' base 10: ec=invalid, value=0, consumed all: false
'0xFF' base 16: ec=ok, value=0, consumed all: false
'FF' base 16: ec=ok, value=255, consumed all: true
'18446744073709551616' base 10: ec=out_of_range, value=0, consumed all: true
```

所以写法是三步：去前缀（自己判断 `0x` / `0b`）→ `from_chars` 解析到 `uint64_t`（先用 64 位，`0xFFFFFFFF + 1` 才能被发现，不会回绕）→ 检查 `ec`、**检查结束指针等于末尾**、检查 `v <= 0xFFFFFFFF`。

### 4.2 一行 → 一条指令

```cpp
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
```

* 助记符转大写用自己的 `to_upper`（ASCII）。`std::toupper(char)` 传负数是 UB，输入里有字节 ≥ 0x80（比如 UTF-8 的 `é`）就会踩到。
* 空白判断同理：自己的 `is_space`。`\r` 也算空白，所以 CRLF 的输入不用特殊处理。
* 内嵌的 NUL 字符既不是空白也不是数字，会落到「格式错误」。
* `try { ... } catch (const std::invalid_argument&)`：`SetBit(32)` 之类由类型的构造函数抛出，在解析边界翻译成 `MalformedProgram`；`MalformedProgram` 不是 `invalid_argument` 的子类，所以不会被这个 `catch` 误接。

## 5. Part 1 + 3：执行

### 5.1 `<bit>` 与手写的位运算

```cpp
// <bit> (C++20): rotate, popcount, leading / trailing zeros.  All defined for 0 and for any rotate count.
#include <bit>
#include <climits>
#include <cstdint>
#include <iostream>

int main() {
    const std::uint32_t x = 0x12345678u;
    std::cout << std::hex << "rotl(x, 4)  = 0x" << std::rotl(x, 4) << "\n";
    std::cout << "rotr(x, 4)  = 0x" << std::rotr(x, 4) << "\n";
    std::cout << "rotl(x, 36) = 0x" << std::rotl(x, 36) << "   (count taken mod 32)\n";
    std::cout << "rotl(x, INT_MAX) = 0x" << std::rotl(x, INT_MAX) << "\n" << std::dec;
    std::cout << "popcount(0xF0F0) = " << std::popcount(0xF0F0u) << "\n";
    std::cout << "countr_zero(0) = " << std::countr_zero(0u) << ", countl_zero(0) = " << std::countl_zero(0u)
              << "   (__builtin_ctz(0) and __builtin_clz(0) are undefined)\n";
    std::cout << "countl_zero(1) = " << std::countl_zero(1u) << ", countr_zero(0x80000000) = " << std::countr_zero(0x80000000u) << "\n";
}
```

```text
rotl(x, 4)  = 0x23456781
rotr(x, 4)  = 0x81234567
rotl(x, 36) = 0x23456781   (count taken mod 32)
rotl(x, INT_MAX) = 0x91a2b3c
popcount(0xF0F0) = 8
countr_zero(0) = 32, countl_zero(0) = 32   (__builtin_ctz(0) and __builtin_clz(0) are undefined)
countl_zero(1) = 31, countr_zero(0x80000000) = 31
```

* `std::rotl(x, s)` / `rotr`：对**任何** `s` 都有定义（取 mod 32），所以 `ROL 36`、`ROL 2147483647` 不需要自己处理。手写 `(x << s) | (x >> (32 - s))` 在 `s == 0`（右移 32 位）和 `s ≥ 32` 时是 UB。
* `std::popcount` / `countr_zero` / `countl_zero`：对 0 有定义。

Part 3 的指令，C++20 标准库里没有现成的函数，自己写（都很短）：

* `COMPRESS`（x86 的 `PEXT`）：只遍历掩码里为 1 的位。`m &= m - 1` 清掉最低位的 1；`countr_zero(m)` 得到它的位置；把 `x` 的那一位依次放到结果的第 0、1、2…位。
* `EXPAND`（`PDEP`）：反过来，把 `x` 的低位依次放到掩码的各个 1 的位置。`expand(compress(x, m), m) == x & m`。
* `BSWAP`：`std::byteswap` 是 C++23，C++20 用移位和掩码拼。
* `REVERSE`：交换相邻位、再交换相邻的 2 位、再交换相邻的 4 位，最后字节翻转。

```cpp
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
```

### 5.2 `apply` / `query` / `run`

```cpp
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
```

* `std::visit(overloaded{lambda...}, u)`：每个备选类型一个 lambda，**漏一个就编译不过**——这是「没有 `default`」的好处：以后新增指令，这里不补分支就过不了编译。
* 每个 lambda 显式写 `-> Reg`：`std::visit` 要求所有分支返回同一个类型。
* **移位**：`i.count >= 32 ? Reg{0} : reg << i.count`。`x << 32` 在 C++ 是 UB（UBSan 会报 `shift exponent 32 is too large for 32-bit type`），不是 Java 的「等于 `x << 0`」，也不是硬件的 0。两种有定义的写法：显式分支，或者提升到 64 位再截断（Part 4 用后者）：

```cpp
// Shifting a 32-bit value by >= 32 is undefined in C++.  Two defined ways to get the hardware answer (0).
#include <cstdint>
#include <iostream>

std::uint32_t shl_branch(std::uint32_t x, int n) { return n >= 32 ? 0u : x << n; }

std::uint32_t shl_wide(std::uint32_t x, std::uint32_t n_clamped_to_32) {
    return static_cast<std::uint32_t>(static_cast<std::uint64_t>(x) << n_clamped_to_32);  // 64-bit shift by <= 32 is defined
}

int main() {
    const std::uint32_t x = 0xFFFFFFFFu;
    std::cout << "shl_branch(x, 32) = " << shl_branch(x, 32) << "\n";
    std::cout << "shl_wide(x, 32)   = " << shl_wide(x, 32) << "\n";
    std::cout << "shl_wide(x, 31)   = 0x" << std::hex << shl_wide(x, 31) << "\n";
    // `x << 32` itself is not run here: UBSan reports "shift exponent 32 is too large for 32-bit type"
}
```

```text
shl_branch(x, 32) = 0
shl_wide(x, 32)   = 0
shl_wide(x, 31)   = 0x80000000
```
* **`~reg`**：`uint32_t` 就是 `unsigned int`，取反后仍是 32 位无符号。如果寄存器是 `uint8_t` / `uint16_t`，整型提升（integer promotion）会先变成 `int`，`~x` 变成一个 32 位的负数：

```cpp
// Small unsigned types are promoted to (signed) int before arithmetic: `~x` and `x << n` do not stay 16 bits wide.
#include <cstdint>
#include <iostream>
#include <type_traits>

int main() {
    const std::uint16_t x = 0x00FF;
    static_assert(std::is_same_v<decltype(~x), int>);
    std::cout << std::hex << "~x as printed        = 0x" << ~x << "   (an int: 0xFFFFFF00)\n";
    std::cout << "~x == 0xFF00 ?         " << std::boolalpha << (~x == 0xFF00) << "\n";
    std::cout << "uint16_t(~x) == 0xFF00 ? " << (static_cast<std::uint16_t>(~x) == 0xFF00) << "\n";

    const std::uint32_t y = 0x000000FFu;
    static_assert(std::is_same_v<decltype(~y), std::uint32_t>);  // uint32_t is unsigned int: no promotion, so a 32-bit register is safe
    std::cout << "~y (uint32_t)         = 0x" << ~y << "\n";
}
```

```text
~x as printed        = 0xffffff00   (an int: 0xFFFFFF00)
~x == 0xFF00 ?         false
uint16_t(~x) == 0xFF00 ? true
~y (uint32_t)         = 0xffffff00
```

* **初值为什么是 `long long` 参数**：`4294967295` 放不进有符号 32 位；而 `static_cast<Reg>(-1LL)` 会悄悄变成 `0xFFFFFFFF`——一个"合法"的寄存器。所以先检查范围，再转换。

## 6. Part 2：格式与整题

```cpp
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
```

* `dec`：`std::to_string(reg)`——`reg` 是无符号，所以 `0x80000000` 打印成 `2147483648`。如果寄存器是 `int32_t`，这里就是 `-2147483648`。
* `hex`：自己填 8 个十六进制数字，永远 8 位、大写。
* `bin`：`std::bitset<32>(reg).to_string()`，自带补零到 32 位。
* `solve`：第一个有效行是初值，其余是程序。只有 `MalformedProgram` 被接住变成 `Malformed Input`；其他异常（比如 `bad_alloc`）不该被吞。

题目是 stdin → stdout 的形态，所以还有一个很薄的 `main`：

```cpp
// stdin -> stdout: first line the initial value, then instructions; prints one line per query and the final register.
#include <iostream>
#include <string>

#include IMPL_HEADER

int main() {
    std::ios::sync_with_stdio(false);
    std::vector<std::string> lines;
    for (std::string line; std::getline(std::cin, line);) lines.push_back(line);
    for (const std::string& out : regsim::solve(lines)) std::cout << out << '\n';
    return 0;
}
```

## 7. Part 4：解码一次，`std::vector<uint32_t>` 操作码

解释器每条指令都要走一遍 `std::visit`（按 variant 的下标跳转）。如果同一个程序要跑很多遍（比如对很多初值），可以先**解码一次**到两个平行的 `uint32_t` 数组：操作码、操作数。

* `NOT` 折叠成 `XOR 0xFFFFFFFF`；`SET b` → `OR (1<<b)`；`CLEAR b` → `AND ~(1<<b)`；`TOGGLE b` → `XOR (1<<b)`。执行时少四种分支。
* 移位位数在解码时 `clamp` 到 `[0, 32]`；旋转位数 `& 31`。
* 执行时用 64 位做移位：`static_cast<Reg>(static_cast<std::uint64_t>(reg) << a)`，`a ≤ 32` 时 64 位移位有定义，左移 32 把原来的 32 位全推到高半部分，截断后全是 0——**没有 `if (count >= 32)` 分支，也没有 UB**。
* 连续的 `uint32_t` 对预取友好；真实的 `Instr`（嵌套 `variant`）占 16 字节，数组里每条指令只占 8 字节。

```cpp
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
```

比较两种表示（同一个随机程序，`-O2`）：

```cpp
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
```

在这个小基准里 opcode 数组大约快 2 倍（`variant` + `visit` 约 205 ms，数组约 88 ms；数字随机器而变，结论是量级）。但注意**两者都有「每条指令一次间接跳转」**：`switch` 编译成跳转表，操作码序列随机时 CPU 的分支预测器经常猜错，这才是随机程序上的主要开销；解码只是去掉了其他开销。

## 8. 和 Java 版的区别

| 点 | Java | C++20 |
|---|---|---|
| 寄存器类型 | `int`（有符号，按无符号解释） | `std::uint32_t`（真无符号） |
| 逻辑右移 | `>>>` | `>>`（无符号类型） |
| 移位位数 ≥ 32 | `<<` 取低 5 位（`x << 32 == x`） | **UB**；必须显式处理 |
| 无符号打印 | `Integer.toUnsignedString` | `std::to_string(uint32_t)` |
| 旋转 | `Integer.rotateLeft` | `std::rotl`（`<bit>`） |
| `popcount` / `ctz` / `clz` | `bitCount` / `numberOfTrailingZeros` / `…LeadingZeros` | `std::popcount` / `countr_zero` / `countl_zero`；`__builtin_ctz(0)` 是 UB |
| compress / expand / reverse / bswap | `Integer.compress` 等 | 标准库没有（`std::byteswap` 是 C++23）：自己写，或 x86 的 `PEXT` / `PDEP` |
| 数字解析 | `Long.parseLong` + 逐字符检查 | `std::from_chars` + 检查结束指针；不认 `+` |
| 指令层次 | `sealed interface` + `record` | `std::variant` + 小结构体 |
| 穷尽匹配 | 模式匹配 `switch`，不写 `default` | `std::visit(overloaded{...})`，漏一个类型编译失败 |
| 记录的校验 | 紧凑构造器抛 `IllegalArgumentException` | 构造函数抛 `std::invalid_argument` |
| 字符分类 | `Character.digit`（Unicode） | 自己写 ASCII 版；`std::isspace(char)` 传负数是 UB |

## 9. 陷阱

1. 用 `int` 当寄存器：`>>` 补符号位，`1 << 31` 变负数，打印出负数。
2. `x << n` 且 `n >= 32`：UB（编译器可以假设它不发生，结果不可预测）。
3. 手写旋转 `(x << s) | (x >> (32 - s))`，`s == 0` 时右移 32 位。
4. `__builtin_ctz(0)` / `__builtin_clz(0)`。
5. `static_cast<uint32_t>(initial)` 之前不检查范围：`-1` 变成 `0xFFFFFFFF`。
6. `from_chars` 不检查结束指针：`12abc` 被当成 12。
7. `0x` 前缀留给 `from_chars`：它不认，`0xFF` 会解析成 0 就停。
8. `std::toupper` / `std::isspace` 直接吃 `char`：字节 ≥ 0x80 时 UB。
9. `uint8_t` / `uint16_t` 寄存器上的 `~x`、`x << n`：整型提升成 `int`。
10. 十进制 `010` 当八进制。
11. `solve` 里 `catch (...)`：把 `bad_alloc` 之类也吞成 `Malformed Input`。
12. 十六进制输出忘记补零 / 用小写。

## 10. 面试官会追问什么（senior）

**Q1. 为什么用 `uint32_t` 而不是 `unsigned int`？** `unsigned int` 的宽度由平台决定（通常 32，但标准只保证 ≥ 16）；`uint32_t` 明确是 32 位。位运算题里宽度是语义的一部分。

**Q2. 对 `uint64_t` 寄存器再做一遍？** 把 `Reg` 换成 `uint64_t`，所有 32 换成 64（用 `std::numeric_limits<Reg>::digits`，不要散落字面量），`0xFFFFFFFF` 换成 `~Reg{0}`；`from_chars` 的范围检查改成「`from_chars` 本身溢出就是 `out_of_range`」。

**Q3. 这段位运算代码有 bug，找一找？** 典型：有符号类型的 `>>`；`1 << 31`；移位位数 ≥ 宽度；`__builtin_clz(0)`；`int` 和 `long long` 混用时的符号扩展（`int` 的 `0x80000000` 转 `uint64_t` 变成 `0xFFFFFFFF80000000`）；`from_chars` 不查结束指针。

**Q4. 为什么解码到数组更快？哪里还会慢？** 去掉了每条指令的类型分发和大对象的读取，折叠了几种指令；但 `switch` 本身是间接跳转，操作码随机时分支预测失败是主要开销。再往下：threaded code（computed goto）、把相邻指令融合成超指令、或者对热点程序直接生成机器码（JIT）。

**Q5. 怎么让 `ROL` 编译成一条指令？** `std::rotl` 在 x86 / ARM 上就是一条旋转指令。手写时用无 UB 的惯用形式 `(x << (s & 31)) | (x >> (-s & 31))`，主流编译器能把它识别成旋转指令，`s == 0` 时也没有 UB。

**Q6. `std::variant` 的 `visit` 开销多大？** 对备选类型很少、`visit` 内联的情况，编译器生成按下标的跳转表；开销接近一次 `switch`。这里的 `Instr = variant<Update, Query>` 是嵌套的，要分发两次（先选 `Update` / `Query`，再选具体类型）。

**Q7. 位板（bitboard）/ 位集（bitset）？** 同一套技巧：`std::bitset<N>`、`uint64_t` 位板（棋盘 64 格）、`countr_zero` + `m &= m - 1` 遍历所有 1 的位。

**Q8. 大端 / 小端对 `BSWAP` 有关系吗？** `BSWAP` 的语义是固定的（翻转字节顺序），与机器无关；有关系的是把寄存器写进字节缓冲区——用 `memcpy` 加 `std::endian` 判断，或者统一用移位拆字节。

## 11. 自测

1. `uint32_t x = 0xFFFFFFFF; x << 32;` 在 C++ 里是什么？Java 里呢？
2. `static_cast<uint32_t>(-1LL)` 是什么？为什么 `run` 的参数是 `long long` 并且先检查范围？
3. `std::from_chars("12abc")` 返回成功吗？怎么才能拒绝它？
4. 为什么 `std::toupper(c)` 不能直接用在 `char` 上？
5. `COMPRESS` 的循环为什么写 `m &= m - 1`？
6. `uint16_t x = 0x00FF; ~x == 0xFF00` 的结果是什么？

<details><summary>答案</summary>

1. C++：UB（位数 ≥ 类型宽度）。Java：位数只取低 5 位，`x << 32 == x`。要硬件语义（0）就必须显式判断，或者用 64 位做移位。
2. `0xFFFFFFFF`——无符号转换按 2^32 取模，不报错，所以一个非法的初值会变成一个"合法"的寄存器。参数用 `long long` 才能先判断 `< 0` 和 `> 0xFFFFFFFF`，再转换。
3. 返回成功，值是 12，结束指针停在 `a`。要拒绝就检查 `end == s.data() + s.size()`。
4. `std::toupper` 的参数必须是 `unsigned char` 的值或 `EOF`；`char` 在多数平台是有符号的，字节 ≥ 0x80 变负数，是 UB。
5. `m - 1` 把最低位的 1 变成 0、其下的 0 全变成 1，与 `m` 相与恰好清掉最低位的 1，每次循环处理一个掩码位，不用扫 32 位。
6. `false`：`x` 先提升成 `int`，`~x` 是 `0xFFFFFF00`（负数），不等于 `0xFF00`。比较前要 `static_cast<uint16_t>(~x)`。

</details>
