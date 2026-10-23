---
id: hl-ld01-false-sharing
node: problems.ld01-spsc-channel
type: qa
step: 6
---
## Q
缓存一致性、伪共享（false sharing）和 cached index 是什么？Java 里怎么填充，实测数据怎么说？

## A
**缓存一致性**：每个核心有自己的缓存，数据按**缓存行**（cache line，x86 常见 64 字节，Apple M 128 字节）搬运。协议（MESI 一类）规定：某核心要**写**一条缓存行时，先让别的核心里的副本失效；别核再读就要从写者重新取。这次跨核搬运约几十纳秒，比普通运算慢两个数量级。

**伪共享**：线程 A 只写 `a`，B 只写 `b`，二者恰在同一条缓存行：A 每写一次让 B 的副本失效，反之亦然。环里 `tail`（生产者写）和 `head`（消费者写）若相邻，每次 `offer` 使消费者核心里 `head` 所在行失效，每次 `poll` 反之。**解决：填充（padding）**，让两变量相隔至少一条缓存行。

**cached index**：即使分开，生产者每次 `offer` 仍要读 `head` 判满，而该行是消费者在写。`head` 只增不减，生产者保存旧 `head`（`cachedHead`）：旧值算出的剩余空位只会偏小不会偏大——「旧值看起来有空位」一定真有；只有「看起来满了」才读真 `head` 刷新。消费者对 `tail` 同理。安全来自**单调性**；效果：队列不是几乎满 / 几乎空时，一批消息只触碰一次对方的缓存行。

**Java 里填充**：没有 `alignas`，用**继承链 + 填充 `long`**（JVM 总把父类字段排在子类字段之前且不跨类重排）：
```java
abstract class RingBase { final long[] buf; final int mask; }                // 只读，放最前面
abstract class PadA extends RingBase { long a01, ..., a15; }                 // 15 个 long = 120 字节
abstract class ProducerFields extends PadA { long tail; long cachedHead; }
abstract class PadB extends ProducerFields { long b01, ..., b15; }
abstract class ConsumerFields extends PadB { long head; long cachedTail; }
abstract class PadC extends ConsumerFields { long c01, ..., c15; }
public final class SpscLongRing extends PadC implements LongQueue { ... }
```
`buf/mask` 只读放最前面的基类，若与 `head` 同行，消费者写 `head` 会使生产者的 `buf` 副本失效。JDK 内部用 `@jdk.internal.vm.annotation.Contended`，用户代码需 `-XX:-RestrictContended`，所以用继承技巧。

**实测**（单变量实验，每线程 2 亿次自增）：相邻（同一缓存行）中位数 1606 / 1757 ms，相隔 128 字节以上 820 / 917 ms，**相邻慢约 2 倍**，且呈**双峰**（~820 与 ~1800，取决于两线程是否在同一核心簇；Apple M 有 P/E 核且 macOS 不能绑核）。

SPSC 五种写法（M 条/秒中位数）：volatile 38、acq/rel 34、acq/rel+填充 27.5、acq/rel+cache 34、acq/rel+cache+填充 44；范围 27–49 大面积重叠——**不要对这类吞吐差异下结论**。仍然填充的理由：伪共享代价真实且大；字段布局取决于 JVM 排布，不填充无法控制是否同行；x86 服务器上收益通常更明显。「微基准要说清测的是什么、噪声多大、取中位数还是最大值。」
