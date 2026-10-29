---
id: uth-java-linkedhashmap-treemap-1-lru
node: java.linkedhashmap-treemap
type: qa
step: 1
---
## Q
**用 LinkedHashMap 写 LRU 缓存**｜Java · OpenJDK 25

`LinkedHashMap` 怎么只用几行就变成 LRU 缓存？底下靠什么保证 O(1)？

## A
**结构。** 就是 `HashMap`，只是每个节点多了 `before`、`after` 两个指针，把所有节点串成一条双向链表。

**细节。**

```java
new LinkedHashMap<>(16, 0.75f, true) {
  protected boolean removeEldestEntry(Map.Entry e) { return size() > 3; }
}
```

- 第三个参数 `accessOrder = true`：每次 `get`、`put` 已有 key，都把节点摘下接到链表尾。
- 每次插入后调用 `removeEldestEntry(链表头)`，返回 `true` 就删掉链表头。
- 实测放入 a、b、c，`get(a)`，再放入 d：剩下 `[c, a, d]`，b 被淘汰。

**为什么。** 哈希表管查找，链表管顺序，两个 O(1) 合起来就是 LC 146 的标准解。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 460 LFU 缓存
