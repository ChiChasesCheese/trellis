---
id: hl-hc07-java21-features
node: problems.hc07-ticker-hash-map
type: qa
step: 18
---
## Q
这个哈希表实现用到哪些 Java 21 特性和 API？各自的好处是什么？

## A
- **record + sealed + 模式匹配 switch + record 模式**：`Parsed permits Ticker(long key), Invalid(String reason)`；合法 / 非法封闭成一个类型，调用方必须处理两种，比返回 `-1` 魔数诚实；测试直接 `assertEquals(new Ticker(…), parse("AAPL"))`。旧写法返回 `long` 非法时 `-1`（易忘检查）或抛异常。
- **switch 表达式**：分支直接 `throw` 或产生值，无 fallthrough。
- **位工具与数学**：`Long.compress`（拼 wire 字段，一条代替 8 次移位掩码）、`Integer.numberOfTrailingZeros`（2 的幂时就是 log₂）、`Integer.highestOneBit`（向上取 2 的幂：`highestOneBit(x - 1) << 1`）、`Math.addExact`。
- **`VarHandle`**：`MethodHandles.byteArrayViewVarHandle(long[].class, BIG_ENDIAN)`，把 `byte[]` 当 `long[]` 读，自带边界检查，不分配 `ByteBuffer`，JIT 内联成一次读取。
- **FFM `Arena` / `MemorySegment`**（预览）：堆外、对齐可控、有边界与生命周期检查。
- **运行时**：`Bench` 预热 / 取最好 / 防死代码消除；`ThreadMXBean` 分配量；逃逸分析与 Generational ZGC。

手写小题：`log2(powerOfTwo)` = `Integer.numberOfTrailingZeros(powerOfTwo)`；`nextPowerOfTwo(x) = x == 1 ? 1 : Integer.highestOneBit(x - 1) << 1`（x ≤ 2³⁰）。

C++ 对应：`std::countr_zero`、`std::bit_ceil`（`<bit>`），x86 上 `pext`；`memcpy` + `bswap`；`__builtin_add_overflow`。
