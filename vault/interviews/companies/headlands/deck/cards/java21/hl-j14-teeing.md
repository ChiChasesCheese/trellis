---
id: hl-j14-teeing
node: java21.j14-stream-api
type: qa
step: 11
---
## Q
`Collectors.teeing` 做什么？写出一次遍历算出 VWAP（总名义金额 / 总数量）所需的代码。

## A
tee 是 T 形三通管：**把同一个流同时喂给两个收集器，最后用一个函数合并两个结果**（Java 12）。

```java
Vwap all = trades.stream().collect(Collectors.teeing(
    Collectors.summingLong(Trade::qty),                   // 收集器 1：总数量
    Collectors.summingLong(t -> Math.multiplyExact(t.pxTicks(), t.qty())),  // 收集器 2：总名义金额
    Vwap::new));                                          // 合并
```
解决「一次遍历得到两个结果，没有可变累加器」：流只能消费一次，没有 `teeing` 时要么收集成 `List` 再遍历两次，要么手写累加器。

实现：累加器同时持有两个下游的中间状态；`finisher` 调两个下游的 `finisher` 再调合并函数；并行下 `combiner` 分别合并两份状态。
