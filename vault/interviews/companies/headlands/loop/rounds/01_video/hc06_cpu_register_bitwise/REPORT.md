# hc06 · REPORT

## 概要

FastPrep 把「CPU Register Bitwise Operations」标为 Headlands 电面题（2025-11-11），1p3a 同日的帖子说第一轮电面是 C++、题目又长又难、内容是
「在给定代码框架里 debug + 位运算」。我们拿到的只有这一句，所以按「一个无符号 32 位寄存器 + 一串操作」重建。
对 Java 候选人，这道题几乎全部是**有符号 / 无符号陷阱**：Java 没有 `uint32_t`。

## 来源与置信度

见 `problem.md`。题目名与一句话描述有证据（中）；指令集、输入输出格式、移位 ≥ 32 的语义、`compress/expand` 扩展、`int[]` 性能版本都是 **(reconstructed)**。

## 逐 Part 思路 + 面试官在探什么

### Part 1 · sealed 指令层次 + 模式匹配 switch

* `Instr` → `Update` / `Query` 两层 sealed；每条指令一个 record，位号 / 位数的范围检查放在紧凑构造器里（非法指令构造不出来）。
* `apply(int reg, Update u)` 是一个**没有 `default` 的 switch 表达式**；新增指令时编译器逼你补分支。
* 语义决定（写进 problem.md，面试时要主动和面试官确认）：`SHL/SHR n ≥ 32` 得 0；`ROL/ROR` 位数 mod 32；`SHR` 逻辑右移。
* **探针**：(1) 你选的模型能不能让“非法状态构造不出来”；(2) `reg << 32` 在 Java 里等于 `reg`（位数只取低 5 位）——你有没有想到；
  (3) `>>` 与 `>>>` 的区别——寄存器最高位为 1 时前者补 1。

### Part 2 · 无符号语义 + 输出格式

* 寄存器永远是 `int`；要“看数值”时才转：`Integer.toUnsignedLong(reg)`、`Integer.toUnsignedString(reg)`。
* `hex`：`"0x" + HexFormat.of().withUpperCase().toHexDigits(reg)`（对 `int` 就是 8 位，自动补零）；`bin`：`Integer.toBinaryString` 不补零，要补到 32 位（`StringBuilder.repeat`）。
* `parseValue`：十进制 / `0x` / `0b`。**不能用 `Integer.parseInt("FFFFFFFF", 16)`**（抛 `NumberFormatException`，它认为超出 `int`），也不能用 `Long.decode`（前导 0 当八进制）；用 `Long.parseLong` + 范围检查 + `(int)` 强转。
* **探针**：转十进制时是否用了无符号；十六进制补零；输入解析的范围检查；“你怎么知道这个输出是对的”（往返测试：`parseValue(hex(x)) == unsigned(x)`）。

### Part 3 · 扩展指令

* `Integer.compress(x, mask)`：把 x 中 mask 为 1 的那些位**按顺序收拢到低位**；`expand` 是反操作：`expand(compress(x, m), m) == x & m`。（JDK 19+；x86 的 BMI2 上可编译为 `PEXT/PDEP` 一条指令，其他平台走软件实现，本机未测其速度。）
* `reverse`（位翻转）、`reverseBytes`（字节序）、`numberOfTrailingZeros/LeadingZeros`（对 0 返回 32）、`bitCount`（`POPCNT` intrinsic）。
* 手算例（测试 `extendedProgramEndToEnd`）：`0x12345678` → BSWAP → `0x78563412`（末尾 0 个数：低字节 `0x12 = 0001 0010`，所以 CTZ=1）→ `COMPRESS 0x0F0F0F0F`（每字节取低半字节：`2,4,6,8`）→ `0x8642` → REVERSE → `0x42610000`（CLZ=1）。
* **探针**：你知不知道标准库已经有这些（不要手写循环）；`Integer.numberOfTrailingZeros(0)` 的约定；`compress/expand` 的语义你能不能用例子讲清楚。

### Part 4 · 性能：解码一次，`int[]`，无分支

* `compile`：`List<Instr>` → 两个平行的 `int[]`（操作码、操作数）；`NOT`、`SET/CLEAR/TOGGLE` 折叠为 `XOR/OR/AND`（指令种类从 18 种降到 14 个操作码）；移位位数 clamp 到 `[0,32]`、旋转位数 `& 31`。
* `execute`：一个循环 + `switch (ops[pc])`（`tableswitch`），不创建对象。移位无分支：`(int)(Integer.toUnsignedLong(reg) << a)`，`a` 已 clamp 到 32，`<< 32` 在 long 里不会被 mod，强转 `(int)` 后恰好为 0——省掉了 `if (n >= 32)`。
* **实测（本机，200 万条指令，5 轮预热后取稳定值）**：

  | 程序形态 | `run`（对象 + 模式匹配） | `execute`（`int[]`） | `compile` |
  |---|---|---|---|
  | 随机 18 种指令 | 21 ms | 14 ms | 17 ms |
  | 随机，仅 14 种“更新型”指令（无 compress/expand/查询） | 17 ms | 11 ms | 16 ms |
  | 固定循环的 14 条指令（操作码周期性） | 9 ms | **1 ms** | 7 ms |

  随机程序只快 1.5 倍，固定模式快 9 倍：说明 `switch` 本身是一次**间接跳转**，操作码序列随机时 CPU 的分支预测器猜错（每次 ≈ 十几个周期），
  `int[]` 省掉的对象指针追逐和类型检查被预测失败吃掉了一大半。**“无分支”是指指令语义内部（移位、位号），不是指分发**；
  真正消除分发开销要换算法（把相邻的 `AND/OR/XOR/NOT/SET/CLEAR/TOGGLE` 融合成 `r = (r & a) ^ x` 一条；或者把整个程序翻译成 JVM 字节码/方法句柄）。
* **探针**：为什么解码一次（解析、类型分派、对象分配都挪出热循环）；`int[]` 对缓存友好在哪（连续、预取）；你会不会诚实地说“分支预测”才是剩下的瓶颈。

## 隐藏测试会打的坑（也是“在代码框架里 debug”最可能的 bug 清单）(reconstructed)

* `>>` 代替 `>>>`：`0xF0000000 >> 4` 得 `0xFF000000`。
* `1 << 31` 是负数；`(1 << b)` 当 `long` 用时先溢出成 `int`（要 `1L << b`）。
* `reg << 32`、`reg >>> 32` 等于 `reg`（位数 mod 32）。
* 把寄存器存成 `int` 却用 `Integer.toString` 输出：`0xFFFFFFFF` 打成 `-1`。
* `long` 版本里忘记 `& 0xFFFFFFFFL`，高位残留，后面的 `SHR` 把垃圾位带回来。
* `Integer.parseInt("FFFFFFFF", 16)` 抛异常；`Integer.parseInt("4294967295")` 同样。
* `Long.decode("010")` = 8（八进制）。
* 旋转手写成 `(x << n) | (x >> (32 - n))`：`>>` 的符号扩展污染、`n == 0` 时 `x >> 32 == x` 把自己 OR 回去。
* `SET/CLEAR/TOGGLE` 位号 32 或 −1 没拒绝。
* `bitCount/ctz/clz` 在 0 上的约定。
* `ROL 36` 与 `ROL 4` 必须相同。

## 复杂度 + 实测时间

解析 O(L)（L = 总字符数），执行 O(m)（m = 指令数），每条指令 O(1)；`compile` O(m) 额外空间 8m 字节。
整个 `reference` 套件（71 个测试，含参数化展开，`perf` 为 200 万条随机指令、20 趟 `execute`）在本机运行约 0.7 s。

## 测试清单

`python3 tools/jtest.py run loop/rounds/01_video/hc06_cpu_register_bitwise --impl reference`：共 **71** 个测试（含参数化展开）。
按 tag（脚本计数）：part1 = 32 · part2 = 29 · part3 = 6 · part4 = 4；另 edge = 52 · fmt = 6 · perf = 1 · conc = 0（本题没有并发部分）。
`part1` 里有一个用 `long` 写的独立 oracle（2 000 轮 × 20 步随机指令）与 `int` 实现逐步对拍。

## Java 21 特性

| id | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| J01 record（含紧凑构造器校验） | 全部指令、`Run`、`Compiled`；`SetBit { checkBit(bit); }` | 非法指令构造不出来；`equals` 白送，测试直接比较 `parseLine("AND 0xFF")` 与 `new And(0xFF)` |
| J02 sealed（两层） | `Instr permits Update, Query`；`Update permits …15 个` | 指令集封闭，加指令时所有 switch 编译报错；旧写法是 enum + 一堆可空字段或 `Object` |
| J03 + J04 模式匹配 switch + record 解构 | `apply`：`case And(var m) -> reg & m`；`run`：`case Update u -> … case Query q -> …` | 一次性判类型 + 取字段，无 `instanceof`/强转/`default` |
| J05 switch 表达式 | `apply`、`query`、`parseLine` | 每个分支是表达式，没有 fallthrough，也没有忘记 `break` 的 bug |
| J13 未命名模式 `_`（预览） | `case Not _ ->`、`case Popcount _ ->` | 声明“不需要这个绑定” |
| J15 位运算与数学小工具 | `Integer.compress/expand/rotateLeft/reverse/reverseBytes/bitCount`、`HexFormat`、`Integer.toUnsignedString/toUnsignedLong`、`Math.clamp(long,int,int)`（21）、`StringBuilder.repeat`（21） | 标准库一行代替手写循环，且是 JIT intrinsic；`clamp` 代替 `Math.min(Math.max(..))` |
| J14 Stream | `Arrays.stream(out).boxed().toList()` | 不可变列表一行 |
| J07 文本块 | 测试里的多行程序 | 输入原样可读 |
| J09 Sequenced Collections | `solve` 里 `body.getFirst()` | 代替 `get(0)` |
| J08 `var` | record 模式里的 `case And(var m)` | 类型由 record 组件决定，不必重复写 |

## 面试官可能的追问

1. **「Java 没有 unsigned int，你怎么办？」**——用 `int` 存 32 个 bit（位模式相同），只在三处“解释为无符号”：右移用 `>>>`，转 long 用 `Integer.toUnsignedLong`，打印用 `Integer.toUnsignedString`；比较用 `Integer.compareUnsigned`。要是寄存器是 64 位，对应 `Long.*Unsigned`。
2. **「`x << 32` 在 Java 里是多少？C++ 呢？」**——Java：位数取低 5 位，`x << 32 == x`；C++：位数 ≥ 位宽是**未定义行为**。两边都不是 0，要自己判断 `n >= 32`，或 clamp 后用 long 移位。
3. **「怎么手写 popcount？」**——`Integer.bitCount` 是 `POPCNT` intrinsic；手写：`x &= x - 1` 每次清掉最低位的 1，循环次数 = 1 的个数（Kernighan）；或 SWAR 并行加法（0x55555555 / 0x33333333 / 0x0F0F0F0F）。
4. **「怎么不用额外变量交换两个寄存器？」**——`a ^= b; b ^= a; a ^= b;`；注意 a、b 是同一个变量时会变 0。
5. **「性能还能怎么优化？」**——解码一次到 `int[]`（已做）；融合相邻的纯位运算为 `(r & a) ^ x`（`AND/OR/XOR/NOT/SET/CLEAR/TOGGLE` 的复合仍是这种形式）；常量折叠；用生成的字节码 / `MethodHandle` 消除分发的间接跳转；批量跑很多寄存器时可以向量化（`jdk.incubator.vector`）。
6. **「如果寄存器是 64 位 / 可配置位宽？」**——`long` + 掩码 `(1L << w) - 1`（w = 64 时 `1L << 64 == 1`，要特判）；所有 `Integer.*` 换成 `Long.*`；位宽作为参数时，每次运算后 `& mask`。
7. **「为什么 `parseValue` 不用 `Long.decode`？」**——它把前导 0 当八进制，接受负号与 `#`；题面是严格的小语言。
