---
id: hl-hc06-compile-execute
node: problems.hc06-cpu-register-bitwise
type: qa
step: 13
---
## Q
Part 4 的 `compile` / `execute` 怎么把程序解码一次到 `int[]`？化简规则和无分支移位怎么写？

## A
**问题**：1000 万条指令或同一程序对大量初值各跑一遍；`run()` 每步取对象（指针追逐）、类型分派、record 解构。**做法**：编译一次，变成两个平行的 `int[]`：`ops[]`（操作码）和 `args[]`（操作数）；热循环只有数组读写和一个 `switch (ops[pc])`（`tableswitch`），不创建对象。`queryCount` 预先数好，一次分配输出数组。

**解码时化简**（指令种类 18 种降到 14 个操作码）：
- `NOT` = `XOR 0xFFFFFFFF`；`SET b` = `OR (1<<b)`；`CLEAR b` = `AND ~(1<<b)`；`TOGGLE b` = `XOR (1<<b)`；
- 移位位数 `Math.clamp(c, 0, 32)`（Java 21）；旋转位数 `c & 31`。

**移位免分支**：
```java
case SHL -> reg = (int) (Integer.toUnsignedLong(reg) << a);   // a ∈ [0, 32]
case SHR -> reg = (int) (Integer.toUnsignedLong(reg) >>> a);
```
`toUnsignedLong` 把 32 位零扩展到 64 位；`long` 移位真移 32 位，`(int)` 强转只留低 32 位，恰好为 0，省掉 `if (n >= 32)`。

热循环：`for (pc...) { int a = args[pc]; switch (ops[pc]) { case AND -> reg &= a; ... case POPCOUNT -> out[q++] = Integer.bitCount(reg); } }`，返回时 `Arrays.stream(out).boxed().toList()` 只装箱一次。

连续的 `int[]` 对缓存友好：读完第 k 个，k+1..k+15 已在缓存行里（64 字节）；`Object[]` 的对象散落堆上。结果必须与 `run` 完全相同（逐程序比较）。复杂度：解析 O(L)，执行 O(m)，`compile` 额外空间 8m 字节。
