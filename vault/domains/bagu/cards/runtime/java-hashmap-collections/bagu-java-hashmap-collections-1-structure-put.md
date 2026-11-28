---
id: bagu-java-hashmap-collections-1-structure-put
node: a.runtime.java-hashmap-collections
type: qa
step: 1
---
## Q
**HashMap · 底层结构与 put 流程**｜必会

面试官：「说一下 Java 的 HashMap 底层是什么结构？put 一个键值对，里面发生了什么？」

## A
**基本回答。** 数组（桶）加链表，JDK 8 起链表过长转红黑树。put：先算 `hash = h ^ (h >>> 16)`（把高 16 位异或进低 16 位，因为下标只取低位，这样高位不同的 key 也能分开），下标 `(n-1) & hash`，n 始终是 2 的幂；桶空直接放；有节点就逐个比 key（hash 相同且 equals），相同覆盖，否则尾插；元素数超过 容量 × 0.75 扩容。默认容量 16 在第一次 put 时才建，阈值 12。判同靠 hashCode 加 equals 两步：hashCode 决定哪个桶，equals 决定桶里哪个是自己。允许一个 null key，hash 为 0，放下标 0。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 272">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">容量 n=16，下标 = (n-1) &amp; hash，取低 4 位</text>
<rect x="30" y="28" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="47.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="84" y="28" width="52" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">red</text>
<rect x="30" y="56" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="47.0" y="70.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="84" y="56" width="52" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="70.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">new</text>
<rect x="30" y="84" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="47.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="84" y="84" width="52" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sale</text>
<text x="47" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">…</text>
<rect x="30" y="140" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="47.0" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<rect x="84" y="140" width="52" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">tag</text>
<rect x="30" y="168" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="47.0" y="182.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<rect x="84" y="168" width="52" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="182.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">hot</text>
<line x1="136" y1="179" x2="154" y2="179" stroke-width="1.2" stroke="currentColor"/>
<polygon points="154.0,179.0 147.0,175.8 147.0,182.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="154" y="168" width="52" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="180.0" y="182.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">vip</text>
<rect x="30" y="196" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="47.0" y="210.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<rect x="84" y="196" width="52" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="210.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">toy</text>
<text x="236" y="183" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">← 尾插在 hot 后</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">put 看桶：空就放；非空逐个比 key</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">相同（hash 相同且 equals）覆盖，否则尾插</text>
</svg>
左边是下标，右边是挂在这个桶里的节点；hot 和 vip 算出同一个下标 12，所以 vip 排在 hot 后面（尾插）。
**业务场景。** 商品标签字典用自定义 `TagKey` 做 key，只重写了 equals；上线后相同标签的 `get` 偶尔命中偶尔为空，因为对象默认 hashCode 各不相同，落到不同桶；补上 hashCode 后恢复。
**容易错。**
- **以为 hashCode 相同就是同一个 key：** 只说明落同一个桶，还要 equals。
- **用可变对象作 key：** 放进去后改了字段，hashCode 变了，原来的桶里再也找不到。
