---
id: hl-hc06-count-reorder
node: problems.hc06-cpu-register-bitwise
type: qa
step: 7
---
## Q
`Integer` 里的 popcount / ctz / clz / reverse / bswap 各自做什么？对 0 和 −1 返回什么？C++ 里对应什么？

## A
- **popcount**：数 1 的个数，`Integer.bitCount(x)`（CPU `POPCNT`）；`bitCount(0)=0`，`bitCount(-1)=32`。
- **ctz**（末尾 0 的个数，即最低的 1 在第几位）：`Integer.numberOfTrailingZeros(x)`，`x==0` 返回 **32**。
- **clz**（前导 0 的个数）：`Integer.numberOfLeadingZeros(x)`，`x==0` 为 32，`x<0` 为 0。
- **reverse**：32 个 bit 整体倒过来，`Integer.reverse(1) == 0x80000000`；`reverse(reverse(x)) == x`。
- **bswap**（字节序翻转）：`Integer.reverseBytes`，`0x12345678 → 0x78563412`（大小端互转）；语义与机器大小端无关，大小端有关的是把寄存器写进字节缓冲区。

C++20：`std::popcount` / `std::countr_zero` / `std::countl_zero`（对 0 都定义良好，返回 32）；**`__builtin_ctz(0)` / `__builtin_clz(0)` 是 UB**；标准库没有 compress / expand / reverse，`std::byteswap` 是 C++23。

手写 popcount：Kernighan `while (x != 0) { x &= x - 1; count++; }`——`x-1` 把最低位的 1 变 0、右边的 0 全变 1，AND 后这些位都是 0，循环次数 = 1 的个数；或 SWAR 并行加法（`0x55555555 / 0x33333333 / 0x0F0F0F0F`）。遍历所有 1 的位：`countr_zero` + `m &= m - 1`（位板 bitboard 常用）。

交换两个寄存器不用临时变量：`a ^= b; b ^= a; a ^= b;`，但 a、b 是同一变量时会变 0。
