---
id: bagu-lru-1-lru-lfu
node: b.cache.lru
type: qa
step: 1
---
## Q
**LRU 缓存 · 数据结构与 Redis 的近似 LRU、LFU**｜必会

面试官：「LRU 缓存用什么数据结构做到 O(1)？LinkedHashMap 怎么实现？Redis 为什么不用精确 LRU，LFU 又是什么？」

## A
**基本回答。** 哈希表加双向链表：哈希表存 key 到节点，链表按使用顺序排；访问就把节点移到表头，超容量删表尾，`get`、`put` 都是 O(1)。Java 用 `LinkedHashMap`，构造时 `accessOrder=true`，重写 `removeEldestEntry`。Redis 不维护全局链表，而是近似 LRU：随机抽 5 个 key（`maxmemory-samples`）淘汰其中最久未访问的（精确 LRU 每次访问都改链表指针、多两个指针的内存，并发代价高）。带统一 TTL 时过期顺序等于写入顺序，从队头清理，访问时惰性检查。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="10" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希表</text>
<rect x="56" y="18" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="35" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k3</text>
<line x1="86" y1="44" x2="86" y2="92" stroke="currentColor" stroke-width="1.2"/>
<polygon points="86,92 83.0,85.7 89.0,85.7" fill="currentColor"/>
<rect x="56" y="96" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k3:C</text>
<rect x="128" y="18" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158" y="35" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1</text>
<line x1="158" y1="44" x2="158" y2="92" stroke="currentColor" stroke-width="1.2"/>
<polygon points="158,92 155.0,85.7 161.0,85.7" fill="currentColor"/>
<rect x="128" y="96" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1:A</text>
<rect x="200" y="18" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="35" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k2</text>
<line x1="230" y1="44" x2="230" y2="92" stroke="currentColor" stroke-width="1.2"/>
<polygon points="230,92 227.0,85.7 233.0,85.7" fill="currentColor"/>
<rect x="200" y="96" width="60" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="230" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k2:B</text>
<rect x="10" y="96" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="27" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头</text>
<rect x="272" y="96" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="289" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">尾</text>
<line x1="44" y1="110" x2="56" y2="110" stroke="currentColor" stroke-width="1.2"/>
<line x1="116" y1="110" x2="128" y2="110" stroke="currentColor" stroke-width="1.2"/>
<line x1="188" y1="110" x2="200" y2="110" stroke="currentColor" stroke-width="1.2"/>
<line x1="260" y1="110" x2="272" y2="110" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最近用</text>
<text x="230" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最久未用</text>
<text x="10" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">get 命中：摘下节点，插到表头</text>
<text x="10" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">put 超容量：删表尾，用它存的 key 删哈希表项</text>
<text x="10" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Redis：随机抽 5 个，淘汰最久未访问的</text>
</svg>
上方的哈希表按 key 直接指向链表节点，下方的链表从头到尾是「最近用」到「最久未用」，高亮的表尾节点是满了之后第一个被淘汰的。
**代码。** `LinkedHashMap` 实现 LRU：
```java
class LRU<K,V> extends LinkedHashMap<K,V> {
  private final int cap; // 容量上限
  LRU(int cap) { super(16, 0.75f, true); this.cap = cap; } // true 表示按访问顺序
  protected boolean removeEldestEntry(Map.Entry<K,V> e) { return size() > cap; }
}
```
**容易错。**
- **节点里不存 key：** 删表尾时不知道从哈希表删哪个。
- **以为 Redis 是严格 LRU：** 它是随机抽样的近似 LRU，没有全局链表。
- **在有扫描型访问的场景用 LRU：** 一次性的大扫描会把热数据挤掉，应换 LFU（Redis 4.0+，按访问频率保热数据）；它用 8 位对数计数器，`lfu-log-factor` 控制递增速度，`lfu-decay-time` 控制衰减，免得曾经很热的数据永远不被淘汰。
- **LinkedHashMap 直接多线程用：** 它线程不安全，简单做法 `Collections.synchronizedMap`，高并发用 Caffeine。

