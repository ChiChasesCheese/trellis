---
id: hl-javaq-f-q26-details
node: java-questions.f-concurrency
type: qa
step: 6
---
## Q
volatile 在硬件层面怎么实现、代价如何？非 volatile 的 `long` 会撕裂吗？volatile 数组的元素是 volatile 吗？
Is a volatile array's content volatile? How is volatile implemented?

## A
- **实现**：靠内存屏障 / 特殊指令，并禁止 JIT 把读提出循环。volatile 写后需要屏障保证 StoreLoad 顺序（x86 上常见为带 lock 前缀的指令或 `mfence`；ARM 上用 `stlr/ldar` 或 `dmb`），所以 volatile 写比普通写贵；volatile 读在 x86 上几乎免费（一般认识）。
- **撕裂**：非 volatile 的 `long` / `double` 在 JLS 里允许被拆成两次 32 位写；64 位 HotSpot 上实际是原子的，但规范不保证——声明为 `volatile` 即保证。
- **volatile 数组**：只有**引用**是 volatile，**元素不是**。要元素级语义用 `VarHandle` 或 `AtomicLongArray`。
