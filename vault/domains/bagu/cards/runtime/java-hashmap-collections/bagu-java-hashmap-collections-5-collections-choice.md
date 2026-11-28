---
id: bagu-java-hashmap-collections-5-collections-choice
node: a.runtime.java-hashmap-collections
type: qa
step: 5
---
## Q
**常用集合 · ArrayList、LinkedList、LinkedHashMap、TreeMap 怎么选**｜追问

面试官：「ArrayList 和 LinkedList 怎么选？LinkedHashMap、TreeMap 分别用在什么场景？」

## A
**基本回答。** 默认用 ArrayList：数组，随机访问 O(1)，尾部追加均摊 O(1)，扩容 1.5 倍（10、15、22、33）。LinkedList 是双向链表，按下标访问 O(n)，只有已持有节点时插入才 O(1)，找节点本身 O(n)，还要存两个指针、缓存不友好，所以通常更慢，几乎不用。LinkedHashMap 是 HashMap 加一条双向链表，保持插入或访问顺序，可当 LRU。TreeMap 是红黑树，按 key 有序，增删查 O(log n)，要排序和区间查询（`floorKey`、`subMap`）时用；不需要顺序用 HashMap，均摊 O(1)。这些集合都不是线程安全的，高并发 LRU 用 Caffeine。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="8" y="8" width="110" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="63.0" y="33.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ArrayList</text>
<text x="128" y="26" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数组，随机读 O(1)</text>
<text x="128" y="44" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">默认选它</text>
<rect x="8" y="62" width="110" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="87.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LinkedList</text>
<text x="128" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">双向链表，按下标 O(n)</text>
<text x="128" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">几乎不用</text>
<rect x="8" y="116" width="110" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LinkedHashMap</text>
<text x="128" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希表 + 双向链表</text>
<text x="128" y="152" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">保持插入或访问顺序，做 LRU</text>
<rect x="8" y="170" width="110" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TreeMap</text>
<text x="128" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">红黑树，增删查 O(log n)</text>
<text x="128" y="206" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">按 key 有序、范围查询</text>
</svg>
每一行是一种集合：左边是名字，右边上一行是结构和复杂度，下一行是什么时候用。
**举个例子。** 容量 2 的 LRU（accessOrder = true），链表头是最久没用的：put a、put b 得 `[a, b]`；get a 把 a 挪到尾部，得 `[b, a]`；put c 后 size 为 3 超过容量，`removeEldestEntry` 返回 true，淘汰头部的 b，剩 `[a, c]`。
```java
class Lru<K, V> extends LinkedHashMap<K, V> {
    private final int cap;
    Lru(int cap) { super(16, 0.75f, true); this.cap = cap; }  // true：按访问顺序
    @Override protected boolean removeEldestEntry(Map.Entry<K, V> e) {
        return size() > cap;                                    // 超容量淘汰最久未访问的
    }
}
```
**容易错。**
- **忘了 accessOrder 传 true：** 默认是插入顺序，读取不更新顺序，LRU 退化成 FIFO。
- **以为 LinkedList 插入 O(1) 所以更快：** 找位置是 O(n)，实际通常更慢。
