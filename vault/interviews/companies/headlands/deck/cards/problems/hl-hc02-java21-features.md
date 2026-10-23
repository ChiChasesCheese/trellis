---
id: hl-hc02-java21-features
node: problems.hc02-merge-k-streams
type: qa
step: 17
---
## Q
合并流实现里用到了哪些 Java 21 特性？各自比旧写法好在哪？

## A
- **record + sealed + 模式匹配 switch + record 模式**：`Poll = Ready | Pending | Done`、`Msg = Item | End | Failed` 是封闭集合，`case Failed<T>(var cause) ->` 一次拆开；旧写法是类 + `instanceof` 链 + 强转，漏一种无提示。`case Ready<T>(var v, _)` 的 `_` 表示不关心该字段（预览）。
- **`instanceof` 模式**：`e instanceof MergeException me ? me : new MergeException(-1, e)`，判断与绑定合一，`me` 只在为真的分支可见。
- **虚拟线程**：source 阻塞在 I/O 时不占 OS 线程，开 k 个很便宜。
- **`StructuredTaskScope`**（预览）：子线程生命周期绑定在 `try` 块，一个失败自动取消其余。
- **未命名变量 `_`**（预览）：`catch (InterruptedException _)`、`case End<T> _`，明说「不用」。
- **Stream API**：`StreamSupport.stream(spliterator, false)`、`.onClose(Runnable)`、`Stream.iterate(seed, f)` 造无限序列、`toList()` 返回不可修改列表。
- **`Comparator` 组合子**：`comparing(h -> h.value).thenComparingInt(h -> h.stream)`，tie-break 写成链。
- `AtomicBoolean.compareAndSet`、`Thread.join(Duration)`（JDK 19+）。
