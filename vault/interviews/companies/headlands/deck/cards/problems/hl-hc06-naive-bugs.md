---
id: hl-hc06-naive-bugs
node: problems.hc06-cpu-register-bitwise
type: qa
step: 11
---
## Q
寄存器模拟最常见的写法（`int` 存寄存器、`Integer.parseInt`、`>>`、`println`）在哪些输入上是错的？

## A
常见写法复杂度 O(m)，没问题，但这些输入是错的：
| 输入 | 期望 | 原写法 | 原因 |
|---|---|---|---|
| 初值 `4294967295` | 合法 | 抛 `NumberFormatException` | `parseInt` 是有符号 int 范围 |
| `AND 0xFFFFFFFF` | 合法 | 抛异常，不认 `0x` 前缀 | 同上 |
| 初值 `0x80000000`，`SHR 31` | 1 | `-1` | `>>` 补符号位 |
| 初值 `1`，`SHL 32` | 0 | 1 | 移位位数只取低 5 位 |
| 终值 `0xFFFFFFFF` | `4294967295` | `-1` | 没用无符号输出 |
| `SET 32` | `Malformed Input` | `1 << 32 == 1` 悄悄置了第 0 位 | 位号越界没检查 |
| 指令 `FOO` | `Malformed Input` | 默默忽略 | 没有 `else` |
| `ROL 36` | 同 `ROL 4` | 没实现 | |

「在代码框架里找 bug」的典型清单：`>>` 代替 `>>>`（`0xF0000000 >> 4` 得 `0xFF000000`）；`1 << 31` 当正数；`(1 << b)` 当 long 用要 `1L << b`；`(int)` 与 `long` 混用；`long` 版本忘记 `& 0xFFFFFFFFL`，高位残留；`Integer.parseInt("FFFFFFFF", 16)`；`Long.decode("010") = 8`；手写旋转的符号扩展污染；`numberOfTrailingZeros(0)` 当成 −1。

C++ 额外：`int` 的 `0x80000000` 转 `uint64_t` 变成 `0xFFFFFFFF80000000`（符号扩展）。

边界清单：寄存器含最高位时的 `SHR / dec / unsigned / 比较`；`SHL 32 / SHR 32 / SHL 33`；`ROL 32 / 36 / 0`；`SET 31` 与位号 32、−1；十进制 `010` 是 10；`0x` 单独出现；`CTZ/CLZ/POPCOUNT` 在 0 与 −1 上。
