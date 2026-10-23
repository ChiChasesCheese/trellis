# hc06 · CPU 寄存器位运算（一个无符号 32 位寄存器 + 一串操作）

## 读题前你需要知道

全部难点来自「32 个二进制位在 Java 里是怎么存的」：补码（two's complement）、有符号与无符号的区别、`<<` `>>` `>>>` 的差别、
掩码（mask）怎么用。你只需要会写基本的 Java（类、方法、循环、`List`）。

## 背景

一个 CPU 寄存器就是 32 个开关（bit）。你拿到它的初值和一串指令，依次执行，最后输出寄存器的值，以及指令里要求输出的计数。
面试官看的是：你有没有把「Java 的 int 是有符号的」这件事处理干净——每一个 `>>`、`<<`、转十进制、转 long 都是潜在的 bug。

## 输入（stdin / `solve(List<String>)`）

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

* 第 1 个有效行（`0xF0`）：初值（十进制 / 0x 十六进制 / 0b 二进制），范围 0..4294967295。
* 其余每行一条指令（`AND 0x3C` 起），助记符不分大小写；空行与 `#` 开头的行忽略。

| 指令 | 语义（`r` = 当前寄存器） | Part |
|---|---|---|
| `AND m` · `OR m` · `XOR m` | `r op m`（m 是 0..2³²−1 的无符号数） | 1 |
| `NOT` | 所有位取反 | 1 |
| `SHL n` · `SHR n` | 逻辑左移 / 逻辑右移（补 0）；**n ≥ 32 → 结果 0** | 1 |
| `ROL n` · `ROR n` | 循环左移 / 右移；位数 mod 32 | 1 |
| `SET b` · `CLEAR b` · `TOGGLE b` | 第 b 位（0 = 最低位）置 1 / 清 0 / 翻转；b ∈ 0..31 | 1 |
| `POPCOUNT` | **输出** r 里 1 的个数（不改 r） | 1 |
| `COMPRESS m` · `EXPAND m` | `Integer.compress/expand(r, m)`：把 m 为 1 的那些位收拢到低位 / 散开 | 3 |
| `REVERSE` · `BSWAP` | 32 位整体翻转 / 字节序翻转 | 3 |
| `CTZ` · `CLZ` | **输出** 末尾 0 的个数 / 前导 0 的个数（r = 0 时都是 32） | 3 |

## 输出

每条「输出型」指令（POPCOUNT / CTZ / CLZ）在程序运行到它时输出一行十进制；最后一行是终值的三种视图，空格分隔：

```
6
4
0x0000000F 15 00000000000000000000000000001111
```

即 `0x` + 8 位大写十六进制，无符号十进制，32 位二进制（全部补零）。输入有任何问题（格式、范围、未知指令、位号越界）→ 只输出 `Malformed Input`。

## Part

| Part | 签名（`RegisterSim`） | 内容 |
|---|---|---|
| 1 | `Instr parseLine(String)` · `List<Instr> parseProgram(List<String>)` · `int apply(int, Update)` · `int query(int, Query)` · `Run run(long, List<Instr>)` · `long parseValue(String)` | 解析成 sealed 指令层次（records），用模式匹配 switch 执行 |
| 2 | `long unsigned(int)` · `String dec/hex/bin/describe(int)` · `List<String> solve(List<String>)` | 无符号语义、输出格式、整题 |
| 3 | `apply`/`query`/`parseLine` 增加 `COMPRESS EXPAND REVERSE BSWAP CTZ CLZ` | 扩展指令（`Integer.compress/expand/reverse/…`） |
| 4 | `Compiled compile(List<Instr>)` · `Run execute(Compiled, long)` | 解码一次到 `int[]`，热循环不分配、移位无分支；结果必须与 `run` 完全相同 |

指令层次（`Instr` sealed → `Update` / `Query` 两个 sealed 子接口）和全部 record 已在 starter 里给出，记录的紧凑构造器负责校验位号 / 位数。

## 边界清单

* 寄存器含最高位（`0x80000000`，在 `int` 里是负数）时的 `SHR`、`dec`、`unsigned`、比较
* `SHL 32` / `SHR 32` / `SHL 33`：Java 的 `<<` 只取位数的低 5 位，`x << 32 == x`
* `ROL 32`、`ROL 36`、`ROL 0`；`SET 31` / `CLEAR 31` / `TOGGLE 31`；位号 32 与 −1
* 初值 `0`、`4294967295`、`4294967296`（非法）、`-1`（非法）；十进制 `010` 是 10 不是八进制；`0x` 单独出现
* `AND 0xFFFFFFFF`（`Integer.parseInt("FFFFFFFF", 16)` 会抛异常，要用 `long`）
* `CTZ` / `CLZ` / `POPCOUNT` 在 0 与 −1 上；`COMPRESS 0` / `COMPRESS 0xFFFFFFFF`
* 空程序；只有注释；多余空白

## 相关变体

* 同一个模拟器，要求对 `uint64_t` 寄存器再做一遍（`long` + `Long.toUnsignedString` + `Long.compareUnsigned`）。
* 「这段代码有 bug，找出来」：典型的有 `>>` 代替 `>>>`、`1 << 31` 当正数、`(int)` 与 `long` 混用、`Integer.parseInt("FFFFFFFF", 16)`。
* 位集（bitset）、位板（bitboard）、flag 枚举——同一套技巧换个包装。

## 考什么

细心。位运算本身一行就写完；评分点是**每一处有符号 / 无符号、移位位数、数字解析的坑你有没有提前想到**，以及 Part 4 里你能不能说清楚
「为什么解码一次到 int[] 更快、哪里还会慢（分支预测）」。
