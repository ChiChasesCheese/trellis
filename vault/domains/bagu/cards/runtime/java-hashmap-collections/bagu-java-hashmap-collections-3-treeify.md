---
id: bagu-java-hashmap-collections-3-treeify
node: a.runtime.java-hashmap-collections
type: qa
step: 4
---
## Q
**HashMap · JDK 8 为什么引入红黑树，阈值是多少**｜追问

面试官：「JDK 8 的 HashMap 里链表会变成红黑树，什么时候变？为什么要变？」

## A
**基本回答。** 链表过长查找退化成 O(n)，红黑树把最坏降到 O(log n)。树化要同时满足：桶里已有 8 个节点、再插入第 9 个，并且数组长度至少 64；不足 64 时先扩容（碰撞多半是容量不够，扩容比建树便宜）。8 的由来：正常哈希下长度达到 8 的概率不到千万分之一，树化只出现在哈希很差或被人构造冲突时。扩容拆桶后某一半不超过 6 个节点退回链表，6 和 8 之间留缓冲，避免临界值附近反复树化退化；删除节点时则看树结构是否小到撑不住（如根的孩子为空）。选红黑树不选 AVL：平衡要求宽松，旋转少，写多读少的桶里更划算。前提：key 实现了 `Comparable`（String、Integer），树里才能二分；不可比较时 hash 相同的节点两边都要找，防御打折。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="60" y="8" width="220" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="21.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">桶里已有 8 个节点</text>
<text x="170.0" y="36.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再插入第 9 个</text>
<line x1="170" y1="42" x2="170" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,62.0 173.2,55.0 166.8,55.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="62" width="160" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数组长度 ≥ 64 吗？</text>
<line x1="130" y1="92" x2="70" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,122.0 77.7,121.7 74.8,116.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="210" y1="92" x2="270" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,122.0 265.2,116.0 262.3,121.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="86" y="112" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">否</text>
<text x="254" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">是</text>
<rect x="8" y="122" width="124" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="138.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先扩容</text>
<text x="70.0" y="153.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不树化</text>
<rect x="208" y="122" width="124" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="270.0" y="138.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">链表转红黑树</text>
<text x="270.0" y="153.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查找 O(log n)</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">扩容拆桶后不超过 6 个：退回链表</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（6 和 8 之间留缓冲，防来回切换）</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">正常哈希下链表长到 8 的概率不到千万分之一</text>
</svg>
链表已有 8 个再来第 9 个，还要看数组够不够大：不到 64 就先扩容，够大才真的变树；高亮的是转成红黑树这一步。
**业务场景。** 规则表用用户提交的字符串做 key，攻击者构造 hash 相同的字符串：`"Aa"` 和 `"BB"` 的 hashCode 都是 2112，任意拼接如 `"AaAa"`、`"BBBB"` 的 hashCode 全是 2031744，成千上万个全落进同一个桶。没有树化时这个桶是几千节点的链表，每次查找扫一遍，CPU 被拖满；有树化后字符串可比较，走二分，仍是对数级。
