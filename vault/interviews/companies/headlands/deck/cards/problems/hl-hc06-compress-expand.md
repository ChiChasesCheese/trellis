---
id: hl-hc06-compress-expand
node: problems.hc06-cpu-register-bitwise
type: qa
step: 8
---
## Q
`Integer.compress(x, mask)` 和 `Integer.expand(v, mask)` 做什么？给一个例子，它们之间有什么性质？

## A
**compress**：取 `x` 中 `mask` 为 1 的那些位，**按顺序**收拢到低位。例：`x = 1011 0110 (0xB6)`，`mask = 1111 0000 (0xF0)`，mask 为 1 的位置 7 6 5 4，取出 x 的这些位 `1 0 1 1` → 结果 `0000 1011 = 0xB`。

**expand** 是反操作：把 `v` 的低位依次放进 `mask` 为 1 的位置，其余补 0。例：`mask = 0xAA`（位置 1 3 5 7），`v = 0b1001`：v 的低位从低到高 1,0,0,1 依次放进位置 1,3,5,7 → `1000 0010 = 0x82`。再对 `x = 0xD6` 做 `compress(x, 0xAA)`：x 在位置 1,3,5,7 的值是 1,0,0,1 → `0b1001 = 9`；`expand(9, 0xAA) = 0x82 = 0xD6 & 0xAA`。

**性质**：`expand(compress(x, m), m) == x & m`。`COMPRESS 0` 得 0，`COMPRESS 0xFFFFFFFF` 得 x 本身（边界要测）。

硬件支持：JDK 19+ 的 `Integer.compress/expand`；x86 BMI2 上编译为 `PEXT` / `PDEP` 一条指令，其他平台走软件实现。C++ 标准库没有，要自己写（循环里用 `m &= m - 1` 每次处理一个掩码位，不用扫 32 位），或用 x86 的 `PEXT/PDEP`。

面试官看的是你知道标准库已有这些，不会写 20 行循环；`Integer.numberOfTrailingZeros(0)` 的约定；能用例子讲清 compress/expand 的语义。Instr 是 sealed，新增这 6 个 record 后 `apply` 和 `query` 的 switch 立刻编译报错，逼你补全。
