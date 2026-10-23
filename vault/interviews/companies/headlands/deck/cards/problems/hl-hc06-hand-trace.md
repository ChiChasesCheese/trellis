---
id: hl-hc06-hand-trace
node: problems.hc06-cpu-register-bitwise
type: qa
step: 2
---
## Q
手算寄存器程序：初值 `0xF0`，依次 `AND 0x3C`、`SHL 4`、`OR 0x0F`、`POPCOUNT`、`NOT`、`SHR 28`、`POPCOUNT`，每步结果与输出是什么？

## A
- `0xF0 = 1111 0000`；`AND 0x3C`（`0011 1100`，逐位都是 1 才是 1）→ `0x30`；
- `SHL 4` → `0x300`；`OR 0x0F`（有一个 1 就是 1）→ `0x30F = 0011 0000 1111`；
- `POPCOUNT` → 2 + 4 = **6**；
- `NOT`（32 位全部取反）→ `0xFFFFFCF0`，在 Java `int` 里是负数；
- `SHR 28`（逻辑右移）→ 只剩最高 4 位 `1111` = `0xF`；`POPCOUNT` → **4**。

终值 `0xF` = 十进制 15，输出：`6`、`4`、`0x0000000F 15 00000000000000000000000000001111`。

注意：`NOT` 之后 `int` 是负数；`SHR` 写成 `>>` 会补 1；`SHL 32` 不是 0。

另一个手算：`0x12345678` → `BSWAP` → `0x78563412`（CTZ：低字节 `0x12 = 0001 0010`，所以 1）→ `COMPRESS 0x0F0F0F0F`（每字节取低半字节：2,4,6,8）→ `0x8642` → `REVERSE` → `0x42610000`（CLZ=1）。
