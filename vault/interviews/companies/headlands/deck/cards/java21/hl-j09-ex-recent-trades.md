---
id: hl-j09-ex-recent-trades
node: java21.j09-sequenced-collections
type: qa
step: 26
---
## Q
"最近成交，从新到旧"的列表用 `ArrayDeque` 保存时，怎么不复制地倒序遍历？

## A
`ArrayDeque.reversed()` 返回倒序视图，从新到旧遍历，**不用复制**：

```java
for (var t : recentTrades.reversed()) System.out.println(t);
```
成交按时间追加到队尾，`reversed()` 就是从最近的开始看。创建视图 O(1)，Java 21 之前要用 `descendingIterator()` 或复制。
