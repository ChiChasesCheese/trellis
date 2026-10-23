---
id: hl-hc04-java21-features
node: problems.hc04-queue-mean-snapshot
type: qa
step: 16
---
## Q
队列均值实现用到哪些 Java 特性（record 紧凑构造器、sealed、record 模式、`yield`、`VarHandle`）？各自的好处与不该用的场景？

## A
- **record**（Java 16）：`Mean`、`I128`、`Push/Pop/Query/Correct`、`Stat`。旧写法两个字段的值类约 40 行且 `equals` 易漏字段。**紧凑构造器**可校验 / 规范化参数（约分）。不能继承别的类、不可变；需要可变状态或继承时不该用。
- **sealed**（Java 17）：普通 `interface Event {}` 谁都能实现，`switch` 永远要 `default`；`sealed ... permits` 让编译器知道所有可能并检查穷尽。
- **switch 模式匹配 + record 模式**（Java 21）：`case Push(var v) -> ...` 类型测试 + 强转 + 拆字段一步完成，`when` 写守卫。只有两三种情况且不会增加时，普通 `if` 更直白。
- **switch 表达式 + `yield`**（Java 14）：`events.add(switch (t[0]) { case "push" -> { ...; yield new Push(...); } case "pop" -> ...; default -> throw ...; })`，每个命令有自己的块，无 fallthrough。
- **未命名模式 `_`**（Java 21 预览，需 `--enable-preview`）：`case Pop _`、`catch (InterruptedException _)`。
- **`VarHandle`**（Java 9）：对任意字段选内存序（`getAcquire/setRelease/compareAndSet/getVolatile`）；比 `volatile` 更精确，只要「发布」语义，不要全序开销。
- **虚拟线程**：`Executors.newVirtualThreadPerTaskExecutor()`。
- `long[]` 数组 SoA 布局避免每节点一个对象。
