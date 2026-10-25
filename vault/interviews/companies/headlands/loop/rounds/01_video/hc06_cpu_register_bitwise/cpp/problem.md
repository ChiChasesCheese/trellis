# hc06 · CPU 寄存器位运算（C++20 版）

一个 CPU 寄存器就是 32 个开关（bit）。给你初值和一串指令，依次执行，输出指令要求的计数，最后输出寄存器终值的三种视图。位运算本身一行就写完，评分点是**每一处有符号 / 无符号、移位位数、数字解析的坑你有没有提前想到**。C++ 版的核心是：寄存器用 `std::uint32_t`，**移位位数大于等于 32 是未定义行为**（undefined behavior，UB），字符分类函数碰到 ≥ 0x80 的字节也是 UB。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `regsim`）；另外还有一个 stdin 到 stdout 的程序形式（见「怎么跑」）。

## 读题前你需要知道

- **补码**（two's complement）：`int` 把最高位当符号位，`0xFFFFFFFF` 作为 `int` 是 −1。32 个 bit 完全一样，只是解释不同。
- **逻辑右移与算术右移**：无符号类型右移补 0（逻辑），有符号类型右移补符号位（算术）。题目要的是逻辑右移。
- **掩码**（mask）：用来选出若干位的 32 位数，`AND` 保留，`OR` 置 1，`XOR` 翻转。
- **无符号运算回绕有定义**，有符号溢出和过宽的移位是 UB。所以每个移位位数都要显式处理。

## 输入与输出

输入：第 1 个有效行是初值（十进制 / `0x` 十六进制 / `0b` 二进制，前缀不分大小写，范围 0..4294967295，`010` 是十进制 10）；其余每行一条指令，助记符不分大小写；空行和 `#` 开头的行忽略；行内可以用空格或制表符分隔，行尾可以有 `\r`。

```
0xF0
AND 0x3C
SHL 4
OR 0x0F
POPCOUNT
NOT
SHR 28
POPCOUNT
```

输出：每条输出型指令（`POPCOUNT` / `CTZ` / `CLZ`）在运行到它时输出一行十进制；最后一行是终值的三种视图，空格分隔：`0x` + 8 位大写十六进制、无符号十进制、32 位二进制（补零）。

```
6
4
0x0000000F 15 00000000000000000000000000001111
```

输入有任何问题（格式、范围、未知指令、位号越界、空输入）→ 只输出一行 `Malformed Input`。

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

## 公共类型（starter 已给出）

```cpp
using Reg = std::uint32_t;                       // 寄存器：恰好 32 位，无符号

template <class Tag> struct Masked  { Reg mask; };            // And Or Xor Compress Expand
template <class Tag> struct Counted { int count; explicit Counted(int); };  // Shl Shr Rol Ror，count < 0 抛 std::invalid_argument
template <class Tag> struct BitOp   { int bit;   explicit BitOp(int); };    // SetBit ClearBit ToggleBit，bit 不在 0..31 抛 std::invalid_argument
struct Not {}; struct Popcount {}; struct Reverse {}; struct ByteSwap {}; struct TrailingZeros {}; struct LeadingZeros {};

using Update = std::variant<And, Or, Xor, Not, Shl, Shr, Rol, Ror, SetBit, ClearBit, ToggleBit, Compress, Expand, Reverse, ByteSwap>;
using Query  = std::variant<Popcount, TrailingZeros, LeadingZeros>;   // 只读，产生一个要打印的数
using Instr  = std::variant<Update, Query>;

struct MalformedProgram : std::runtime_error {};
struct Run { Reg reg; std::vector<int> outputs; };    // 终值 + 每个 Query 的输出（按程序顺序）
```

「这条指令会不会改寄存器」是类型本身的事实：`Update` 改，`Query` 不改。类型的构造函数负责校验位号和位数，非法指令构造不出来。

## Part 1 · 解析与执行

| 签名 | 要求 |
|---|---|
| `Reg parse_value(std::string_view)` | 十进制 / `0x` / `0b`，范围 0..0xFFFFFFFF，否则抛 `MalformedProgram` |
| `Instr parse_line(std::string_view)` | 一行一条指令；助记符不分大小写；操作数个数或值不对抛 `MalformedProgram`（类型构造函数抛的 `std::invalid_argument` 要翻译过来） |
| `std::vector<Instr> parse_program(const std::vector<std::string>&)` | 跳过空行和 `#` 开头的行 |
| `Reg apply(Reg, const Update&)` | 执行一条更新指令 |
| `int query(Reg, const Query&)` | 执行一条查询指令，返回要打印的数 |
| `Run run(long long initial, const std::vector<Instr>&)` | 初值不在 0..0xFFFFFFFF 抛 `std::invalid_argument` |

- `parse_line("and 255")` 等于 `And{255}`；`"  OR   0b1010 "`、`"Xor 0XF0"` 都能解析；`parse_line("\tshl\t3\r\n")` 等于 `Shl(3)`。
- 这些行必须是 `MalformedProgram`：空行、`FOO`、`AND`（缺操作数）、`AND 1 2`、`NOT 3`、`POPCOUNT 1`、`SHL -1`、`SHL 1.5`、`SET 32`、`SET -1`、`CLEAR 99`、`TOGGLE 3x`、`AND 0x1FFFFFFFF`、`AND 4294967296`、`AND -1`、`AND 0x`、`AND 0b2`、`SHL 99999999999`。
- 掩码是无符号 32 位数：`AND 0xFFFFFFFF`、`OR 2147483648`、`AND 4294967295` 都合法。
- `apply(0xF0000000, Shr(4))` 得 `0x0F000000`（逻辑右移）；`apply(0x80000000, Shl(1))` 得 0；`apply(0x80000000, Shr(31))` 得 1。
- `Rol(4)` 作用于 `0x12345678` 得 `0x23456781`，`Ror(4)` 得 `0x81234567`；`Rol(32)`、`Ror(64)`、`Rol(0)` 都得原值；`Rol(36)` 等于 `Rol(4)`。
- `SetBit(31)` 作用于 0 得 `0x80000000`；`ClearBit(31)` 作用于 `0xFFFFFFFF` 得 `0x7FFFFFFF`；`ToggleBit(31)` 对 `0x80000000` 得 0。
- 样例程序：初值 `0xF0`，输出 `{6, 4}`，终值 `0xF`。
- 初值：`run(0xFFFFFFFF, {})` 的 `reg` 是 `0xFFFFFFFF`；`run(-1, {})` 和 `run(1LL << 32, {})` 抛 `std::invalid_argument`。
- C++ 专属测试：
  - **移位位数 ≥ 32**：`Shl(n)` / `Shr(n)` 对 n ∈ {32, 33, 64, 1000, INT_MAX} 都得 0；`Shl(31)` 作用于 `0xFFFFFFFF` 得 `0x80000000`。UBSan 开着，一触发 UB 就终止。
  - **旋转位数任意大**：`Rol(n)` 对 n ∈ {0, 32, 64, INT_MAX, INT_MAX − 1} 都等于 `Rol(n & 31)`。
  - **`from_chars` 要严格**：`AND 12abc`、`AND 0x1g`、`AND +1`、`SHL +1`、`SHL 1x`、`SET 3.0` 都是 `MalformedProgram`；`parse_value(" 7 ")` 得 7（两端空白会被去掉）；`0x` 后面 32 个十六进制位（前导 0 加 `FF`）得 255；`0x` 后面 41 个 `0` 超过 40 位的上限，抛 `MalformedProgram`。
  - **≥ 0x80 的字节和 NUL**：`"\xC3\xA9ND 1"`、`"AND 0x\xFF"`、`"\xFF"`、带内嵌 NUL 的行，都只是格式错误，不能是 UB。
  - **初值不能因为窄化而回绕**：`-1`、`-4294967295`、`4294967296`、`2^32 + 5`、`LLONG_MIN`、`LLONG_MAX` 都要抛 `std::invalid_argument`，不能被 `static_cast<uint32_t>` 变成「合法」的寄存器。
  - 随机 2000 轮、每轮 20 步，和 64 位 oracle 逐步对拍。

## Part 2 · 无符号语义与输出格式

| 签名 | 要求 |
|---|---|
| `std::uint64_t unsigned_of(Reg)` | 无符号数值 |
| `std::string dec(Reg)` | 无符号十进制 |
| `std::string hex(Reg)` | `"0x"` + 8 位大写十六进制 |
| `std::string bin(Reg)` | 32 位二进制，补零 |
| `std::string describe(Reg)` | `hex dec bin`，空格分隔 |
| `std::vector<std::string> solve(const std::vector<std::string>&)` | 整题：第一个有效行是初值，其余是程序；每条 Query 一行，最后一行 `describe(终值)`；任何问题返回 `{"Malformed Input"}` |

- `hex(255)` 是 `0x000000FF`；`hex(0xDEADBEEF)` 是 `0xDEADBEEF`；`bin(5)` 是 `00000000000000000000000000000101`。
- `dec(0xFFFFFFFF)` 是 `4294967295`，`dec(0x80000000)` 是 `2147483648`。
- `describe(15)` 是 `0x0000000F 15 00000000000000000000000000001111`。
- `parse_value`：`"010"` 是 10；`"0Xff"` 是 255；`"0b101"` 是 5。这些抛 `MalformedProgram`：`""`、`-1`、`+1`、`0x`、`0b`、`0b2`、`0xG`、`4294967296`、`0x100000000`、`99999999999999999999`、`1_000`、`12 3`。
- 往返：对 1000 个随机值，`parse_value(hex(x))`、`parse_value(dec(x))`、`parse_value("0b" + bin(x))` 都等于 `x`。
- `solve({"0"})` 得一行 `0x00000000 0 000...0`；`# initial`、`0`、空行、`SET 31` 得 `0x80000000 2147483648 1000...0`；`solve({"4294967295"})` 得全 1。
- `solve` 对这些返回 `{"Malformed Input"}`：空输入、只有注释、`-5`、`4294967296`、`abc`、初值后跟 `FOO`、`AND`（缺操作数）、`SET 32`、`SHL -1`、以及 ≥ 0x80 的字节（`"\xFF"`）。
- C++ 专属测试：`solve({"0xF0\r", "SHR\t4\r", "\r", "# c\r"})` 必须得 `0x0000000F 15 000...1111`（CRLF 和制表符都要认）。

## Part 3 · 扩展指令

在 `parse_line` / `apply` / `query` 里加上 `COMPRESS` `EXPAND` `REVERSE` `BSWAP` `CTZ` `CLZ`。

- `Compress{0xF0}` 作用于 `0xB6` 得 `0xB`（取高半字节）；`Expand{0xF0}` 作用于 `0xB` 得 `0xB0`。
- 掩码 `0xA4`（二进制 1010 0100，三个位置 2、5、7）：寄存器为 `0x84` 时收拢后得 5（从低位到高位依次是 1、0、1）；寄存器为 `0xA4` 时得 7。
- `Compress{0}` 和 `Expand{0}` 都得 0；掩码为 `0xFFFFFFFF` 时两者都得原值。
- `expand(compress(x, m), m) == x & m`；5000 个随机 (x, m) 和逐位循环 oracle 对拍。
- C++20 没有标准的 compress / expand（`std::byteswap` 是 C++23）：要自己写。
- `Reverse` 作用于 1 得 `0x80000000`，作用于 `0x0F` 得 `0xF0000000`；`ByteSwap` 作用于 `0x12345678` 得 `0x78563412`；两者都是对合（做两次回到原值）。
- `CTZ` / `CLZ`：寄存器为 0 时都是 32；`CTZ(8)` 是 3；`CTZ(0x80000000)` 是 31；`CLZ(1)` 是 31；`CLZ(0xFFFFFFFF)` 是 0。`POPCOUNT(0xFFFFFFFF)` 是 32。
- 端到端：`0x12345678`、`BSWAP`、`CTZ`、`COMPRESS 0x0F0F0F0F`、`REVERSE`、`CLZ`，输出 `1`、`1`、`0x42610000 1113653248 01000010011000010000000000000000`。
- C++ 专属测试：寄存器为 0 时 `CTZ`、`CLZ`、`POPCOUNT` 依次输出 `32, 32, 0`（`__builtin_ctz(0)` 是 UB，不能直接用）。

## Part 4 · 解码一次，热循环不分配

```cpp
struct Compiled {
    std::vector<std::uint32_t> ops;     // 操作码
    std::vector<std::uint32_t> args;    // 操作数
    std::size_t query_count = 0;
};
```

| 签名 | 要求 |
|---|---|
| `Compiled compile(const std::vector<Instr>&)` | 解码一次。`NOT` 和 `SET` / `CLEAR` / `TOGGLE` 可折叠成 `XOR` / `OR` / `AND`；移位位数夹到 [0, 32]，旋转位数 `& 31` |
| `Run execute(const Compiled&, long long initial)` | 热循环：读数组、一个 `switch`，没有 `variant`，没有逐条指令的分配。结果必须和 `run` 完全相同；初值不在范围内抛 `std::invalid_argument` |

- 提示（starter 已给）：位数夹到 ≤ 32 之后，用 `uint64_t` 做移位再截断，既没有 `if (count >= 32)` 分支，也没有 UB。
- 随机 300 个种子、每个 60 条指令（18 种指令都出现，移位位数最大 69），`execute(compile(p), init)` 等于 `run(init, p)`。
- 空程序：`execute(compile({}), 0xFFFFFFFF)` 的 `reg` 是 `0xFFFFFFFF`，没有输出。`{Shl(32), Popcount}` 从 `0xFFFFFFFF` 开始得 `reg = 0`、输出 `{0}`。
- 位数边界：n ∈ {0, 1, 31, 32, 33, 63, 2000000000, INT_MAX} 对 `Shl` `Shr` `Rol` `Ror` 都和 `run` 一致。
- 折叠后的数组长度：`{SetBit(4), ClearBit(0), ToggleBit(1), Not, Popcount}` 编译后 `ops` 和 `args` 各 5 个，`query_count` 是 1；同一个 `Compiled` 可以对不同初值重复执行。
- C++ 专属测试：`ops = {99}` 这种被破坏的数组，`execute` 要抛 `std::logic_error`，不能乱跳。
- 性能：200 万条随机指令，`compile` 加 20 遍 `execute` 在 2 秒内，`run` 也在 2 秒内，结果相同。

## C++ 专属：类型本身

- `Instr` 要是平凡可拷贝的（trivially copyable）、移动构造不抛异常；`sizeof(Instr) ≤ 16`，`sizeof(Update) ≤ 8`。
- 无符号回绕有定义：`Reg{0} - 1` 是 `0xFFFFFFFF`，等于 `Not` 作用于 0 的结果。

## 边界清单

- 寄存器含最高位（`0x80000000`）时的 `SHR`、`dec`、`unsigned_of`
- `SHL 32` / `SHR 32` / `SHL 33`；`ROL 32`、`ROL 36`、`ROL 0`
- `SET 31` / `CLEAR 31` / `TOGGLE 31`；位号 32 与 −1
- 初值 `0`、`4294967295`、`4294967296`（非法）、`-1`（非法）；十进制 `010`；`0x` 单独出现
- `AND 0xFFFFFFFF`、`AND 4294967296`
- `CTZ` / `CLZ` / `POPCOUNT` 在 0 与 `0xFFFFFFFF` 上；`COMPRESS 0` / `COMPRESS 0xFFFFFFFF`
- 空输入、只有注释、多余空白、CRLF、制表符、最后一行没有换行
- ≥ 0x80 的字节、内嵌 NUL

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc06_cpu_register_bitwise          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc06_cpu_register_bitwise --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc06_cpu_register_bitwise --tag cpp   # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc06_cpu_register_bitwise             # 全部
```

**stdin → stdout 形式**：`cpp/main.cpp` 读入全部 stdin 的行，调用 `regsim::solve`，每个结果一行写到 stdout。你的 `solve` 写好后这样跑（`--impl` 默认是 reference，用你自己的实现要写 `--impl work`）：

```bash
python3 tools/cpptest.py main loop/rounds/01_video/hc06_cpu_register_bitwise --impl work < loop/rounds/01_video/hc06_cpu_register_bitwise/cpp/cases/sample.in
```

`cpp/cases/` 里每个 `NAME.in` 配一个 `NAME.out`，对拍时输出必须逐字节相同：

| 用例 | 考什么 |
|---|---|
| `sample` | 题面样例 |
| `extended` | Part 3 的扩展指令，输出 `1`、`1` 和终值 `0x42610000 …` |
| `shift32` | `0xFFFFFFFF` 先 `SHL 32` 得 0，再 `SET 31`、`SHR 31` 得 1 |
| `zero_register` | 初值 4294967295 取反得 0，`CLZ` 和 `CTZ` 都是 32 |
| `bad_bit` | `SET 32`，输出 `Malformed Input` |
| `empty_stdin` | 空输入，输出 `Malformed Input` |
| `crlf_no_trailing_newline` | 以 `#` 注释开头，CRLF 行尾，制表符分隔，最后一行没有换行 |

测试编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 同一个模拟器改成 `uint64_t` 寄存器：位宽用 `std::numeric_limits<Reg>::digits`，不要散落字面量 32。
- 「这段位运算代码有 bug，找出来」：有符号类型的 `>>`、`1 << 31`、移位位数 ≥ 宽度、`__builtin_clz(0)`、`from_chars` 不查结束指针。
- 位集（`std::bitset`）、位板（bitboard）、flag 枚举：同一套技巧换个包装。
