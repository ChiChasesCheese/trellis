---
id: structure-storage-chm-compound-ops
node: structure.storage
type: qa
---
## Q
你制造了钱包存储一个 `ConcurrentHashMap<UserId, Long>` 并宣称它是线程安全的。为什么 `map.put(user, map.get(user) + amount)` 仍然失去钱，正确的调用是什么?

## A
`ConcurrentHashMap` 制造每一个**单独的**调用原子的 — 不是**获得-然后-放置化合物**。两个并发存款都读取 100，都写 100+x；一个存款消失（丢失的更新）。

```java
map.merge(user, amount, Long::sum);          // 原子的读-改-写
map.computeIfAbsent(user, u -> new Wallet())  // 原子的检查-然后-插入
```

`compute`/`merge`/`putIfAbsent` 每个关键原子地运行。如果一个操作跨越**多个关键**（在两个钱包之间转移），没有地图方法保存你 — 你回到明确的锁加上有序获得。
