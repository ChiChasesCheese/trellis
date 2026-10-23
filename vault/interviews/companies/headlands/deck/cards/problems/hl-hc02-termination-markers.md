---
id: hl-hc02-termination-markers
node: problems.hc02-merge-k-streams
type: qa
step: 11
---
## Q
怎样保证合并器不会永远等一个已经死掉的生产者？终止标记（sealed 消息类型）的写法是什么？

## A
生产者要告诉合并器三件事之一：一个元素、正常结束、出错。用 `sealed interface Msg permits Item, End, Failed` 表示（用 `null` 或特殊值会混乱，因为元素本身可能是 `null`；用类型区分则 `switch` 时编译器检查处理全）。`End` 和 `Failed` 是**终止标记**。

生产者循环：
```java
try {
    while (src.hasNext()) { ...; q.put(new Item<>(v)); }
    q.put(new End<>());
} catch (InterruptedException _) {
    // close() 叫我们走，没人在听了
} catch (Throwable t) {
    q.put(new Failed<>(t));   // 留遗言
}
```
无论成功、失败还是被取消，队列最后一定有 `End` 或 `Failed`（整体被取消除外）。合并器读到 `Failed` 抛 `MergeException(流编号, cause)`（先输出该流失败前已入队的元素）并自动 `close()`，之后 `tryNext/next` 抛 `IllegalStateException`。

口述：「阻塞在不保证会结束的事件上，就要设计谁来保证它结束——这里是生产者的 finally 和关闭时的中断。」另可给 `next` 加超时 `poll(timeout)`。
