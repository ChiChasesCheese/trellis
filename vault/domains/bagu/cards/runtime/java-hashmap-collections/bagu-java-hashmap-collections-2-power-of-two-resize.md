---
id: bagu-java-hashmap-collections-2-power-of-two-resize
node: a.runtime.java-hashmap-collections
type: qa
step: 2
---
## Q
**HashMap · 为什么容量是 2 的幂，扩容怎么做**｜必会

面试官：「HashMap 的容量为什么总是 2 的幂？扩容的时候元素怎么搬迁，要重新算哈希吗？」

## A
**基本回答。** 容量是 2 的幂时，`(n-1) & hash` 等价取模但更快，且 n-1 的低位全是 1（16 → `1111`），下标取决于 hash 的全部低位，分布均匀；n=10 则 n-1=`1001`，只能得到 0、1、8、9，其余桶永远空，碰撞暴增。传入的初始容量会被调成不小于它的 2 的幂（100 得 128）。元素数超过 容量 × 0.75（负载因子，空间与碰撞的折中）就翻倍；翻倍后下标只多看 hash 的一位，该位用 `hash & 旧容量` 判断：0 留原下标，非 0 去「原下标 + 旧容量」，不用重算哈希，一条链拆成低位、高位两条且保持顺序。扩容是 O(n) 的一次性搬迁，造成这次 put 的延迟尖刺；已知 N 个元素就提前指定容量，JDK 19 起 `HashMap.newHashMap(N)` 按负载因子算好。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扩容：容量 16 → 32，只多看 hash 的第 5 位</text>
<text x="8" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">旧表 n=16</text>
<rect x="8" y="50" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="28.0" y="64.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<rect x="58" y="50" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="64.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">hot</text>
<line x1="102" y1="61" x2="114" y2="61" stroke-width="1.2" stroke="currentColor"/>
<polygon points="114.0,61.0 107.0,57.8 107.0,64.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="114" y="50" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="136.0" y="64.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">vip</text>
<text x="8" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新表 n=32</text>
<rect x="8" y="108" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="28.0" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<rect x="58" y="108" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">hot</text>
<rect x="8" y="142" width="40" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="28.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">28</text>
<rect x="58" y="142" width="44" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">vip</text>
<line x1="80" y1="72" x2="80" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,106.0 83.2,99.0 76.8,99.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="136" y1="72" x2="136" y2="153" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="136" y1="153" x2="104" y2="153" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="104.0,153.0 111.0,156.2 111.0,149.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="150" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 5 位是 0：留在 12</text>
<text x="150" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 5 位是 1：去 12+16=28</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">怎么判断：hash &amp; 旧容量(16)</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hot 低 5 位 0 1100，结果 0</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">vip 低 5 位 1 1100，结果非 0</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不用重新算哈希，两条链保持原顺序</text>
</svg>
旧表下标 12 的链上有 hot 和 vip；翻倍后看 hash 新参与的第 5 位：0 留在 12，1 去 12+16=28，链被拆成两条。
**业务场景。** 聚合任务每个窗口要放约一百万个计数 key：默认容量 16 要翻倍 17 次（到 2^21，阈值 1572864 才够），每次整表搬迁，窗口结束时延迟抖动明显；按预估大小一次建好，抖动消失。
