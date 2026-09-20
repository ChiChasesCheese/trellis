---
id: concurrency-check-then-act
node: concurrency.model
type: qa
---
## Q
```java
if (!map.containsKey(key)) {
    map.put(key, createExpensive(key));
}
```
`map` 是 `ConcurrentHashMap`，所以每次调用都是线程安全的。bug 在哪，怎么修？

## A
**Check-then-act 竞态**：两个线程都在对方 put 之前通过了检查，于是两个都创建了值，其中一个覆盖掉另一个。一个*复合*操作并不会因为每一步都原子就变得原子。

- 修法：换成一个原子操作 —— `computeIfAbsent(key, k -> createExpensive(k))`（或 `putIfAbsent`）。
- 或者拿一把锁，同时罩住**检查和动作两步**。

`volatile` 在这里帮不上忙 —— 它解决的是可见性，不是原子性。
