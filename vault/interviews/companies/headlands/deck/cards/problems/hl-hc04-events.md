---
id: hl-hc04-events
node: problems.hc04-queue-mean-snapshot
type: qa
step: 8
---
## Q
事件流 Part 2 里，`Event` 怎么建模？`Correct`（修正快照）的语义和实现、解析错误的处理是什么？

## A
把操作序列做成数据：
```java
public sealed interface Event permits Push, Pop, Query, Correct {}
public record Correct(List<Long> contents) implements Event {
    public Correct { contents = List.copyOf(contents); }
}
switch (e) {
    case Push(var v) -> q.push(v);
    case Pop _ -> q.pop();
    case Query _ -> out.add(q.isEmpty() ? new Empty() : new Value(q.mean()));
    case Correct(var contents) -> { q = new QueueMean(); for (long v : contents) q.push(v); }
}
```
- `sealed` 让 `switch` 穷尽、不需 `default`，加第五种事件时编译报错。
- **`Correct` 语义**：丢掉此前整段逻辑历史，队列内容 = 快照给的列表；实现是换一个新的 `QueueMean`。也可读作「快照是某时刻整个队列的真实内容，用来纠正之前积累的误差」，本质同一操作。
- `List.copyOf` 做**防御性拷贝**且拒绝 `null`（立刻抛 NPE）；不拷贝则调用者之后改原列表，历史被悄悄改写。
- 复杂度：事件 O(1)，快照 O(快照长度)，总 O(输入总大小)，是下界。
- 空队列上 `Pop` 抛 `NoSuchElementException`；`snapshot` 后不带数字表示清空；快照里含 `Long.MAX_VALUE` 要靠 128 位和。

**解析**：`push N` / `pop` / `mean` / `snapshot [N ...]`，空行忽略；每种错误（缺参数、非数字、超出 `long`、未知命令）都带行号（从 1 起）`"line k: …"`。`NumberFormatException` 是 `IllegalArgumentException` 的子类，一个 `catch` 统一加前缀。

渲染用嵌套 record 模式加守卫：`case Value(QueueMean.Mean(var n, var d)) when d == 1 -> n.toString();`。
