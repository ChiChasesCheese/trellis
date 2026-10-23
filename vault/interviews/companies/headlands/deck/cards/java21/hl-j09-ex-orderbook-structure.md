---
id: hl-j09-ex-orderbook-structure
node: java21.j09-sequenced-collections
type: qa
step: 23
---
## Q
订单簿里怎么用 `SequencedMap` 表示买盘 / 卖盘和一个价位上的排队？写出字段声明。方法参数为什么写 `SequencedMap` 而不是 `TreeMap`？

## A
```java
// 买盘价格从高到低，卖盘从低到高；两者的「最优价」都是 firstEntry()
final SequencedMap<Long, Level> bids = new TreeMap<>(Comparator.reverseOrder());
final SequencedMap<Long, Level> asks = new TreeMap<>();

static final class Level {
    final SequencedMap<Long, Long> fifo = new LinkedHashMap<>();   // 一个价位上的排队：id -> 剩余数量
    long total;
}
```
- 买盘用 `reverseOrder()`，最优价永远在头部，`firstEntry()` 就是最优价；
- 一个价位上用 `LinkedHashMap` 保持**时间优先**的排队顺序；
- 方法参数写 `SequencedMap` 是为了**只暴露需要的能力**：`bids` 和 `asks` 共用 `book(Side)`，调用方不关心底层是 `TreeMap`。
