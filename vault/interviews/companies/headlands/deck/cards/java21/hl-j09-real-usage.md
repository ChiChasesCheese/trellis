---
id: hl-j09-real-usage
node: java21.j09-sequenced-collections
type: qa
step: 32
---
## Q
真实代码里 Sequenced Collections 主要用在哪里？`Comparator.reversed()` 和 Sequenced 的 `reversed()` 是一回事吗？

## A
- **订单簿**（用得最重）：价位里的排队 `SequencedMap<Long, Node> fifo = new LinkedHashMap<>()`；买盘 / 卖盘 `TreeMap` 声明为 `SequencedMap`，`firstEntry` / `pollFirstEntry` 就是"最优价"，买盘用 `reverseOrder` 让最优价永远在头部；加量用 `putLast` 重新排队。
- **解析后取首行**：`long initial = parseValue(body.getFirst());`，`body` 是 `stream...toList()` 的 `List<String>`，`getFirst()` 代替 `body.get(0)`。

**不是一回事**：`Comparator.reversed()` 返回反序的比较器；Sequenced 的 `reversed()` 返回集合的倒序视图。别混淆。
