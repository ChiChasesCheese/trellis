---
id: hft-cpp-atomics-x86-cost
node: cpp.atomics
type: qa
step: 3
---
## Q
在 x86 上，`relaxed`、`acquire`、`release`、`seq_cst` 的原子读写分别编译成什么指令？为什么说“acquire/release 在 x86 上几乎免费”，而 `seq_cst` 的写要付出代价？

## A
x86 的内存模型叫 TSO（total store order，全存储序）：硬件只允许一种重排——“较早的写”可以排在“较晚的读”之后。其余顺序硬件本来就保证。

结果：
- **load**（relaxed 或 acquire 或 seq_cst）：都是普通的 `mov`。
- **store**（relaxed 或 release）：也是普通的 `mov`。
- **seq_cst 的 store**：必须禁止“写后读”重排，编译成 `xchg`（隐含 `lock`）或 `mov` 加 `mfence`，需要等存储缓冲排空，约十几到几十个周期。
- **读-改-写**（`fetch_add`、CAS）：无论哪个序，都是带 `lock` 前缀的指令，代价相近。

所以在 x86 上：用 acquire/release 取代 seq_cst，**省掉的主要是写操作那一次栅栏**。在弱内存序的 ARM 上，acquire/release 要用专门指令（`ldar`/`stlr`），relaxed 才是最便宜的，选对序的收益更明显。
