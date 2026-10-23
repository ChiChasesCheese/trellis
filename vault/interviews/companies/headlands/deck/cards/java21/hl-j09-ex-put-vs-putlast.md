---
id: hl-j09-ex-put-vs-putlast
node: java21.j09-sequenced-collections
type: qa
step: 25
---
## Q
订单簿里"部分成交"和"加量"分别该用 `LinkedHashMap` 的 `put` 还是 `putLast`？为什么？

## A
- **部分成交用 `put`**：对已存在的 key 只改值，位置不变，订单仍在队头，保持时间优先；
- **加量用 `putLast`**：加量等于重新排队，`putLast` 把已存在的 key 挪到队尾，时间优先被重置。

```java
lv.fifo.putLast(id, newQty);       // 加量：挪到队尾
```
这正是 `put` 与 `putLast` 对已存在 key 行为不同的实际用途。例：id=2 加量两次后排到 id=5 后面。
