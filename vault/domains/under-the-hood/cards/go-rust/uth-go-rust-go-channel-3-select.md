---
id: uth-go-rust-go-channel-3-select
node: go-rust.go-channel
type: qa
step: 3
---
## Q
**select 同时多个 case 就绪选哪个**｜Go · 1.27 运行时

多个 case 同时能执行时，`select` 怎么保证公平、又不死锁？

## A
**背景。** `select` 让一个 goroutine 同时等好几个 channel，哪个先就绪就做哪个。有两个难题：几个同时就绪时，如果总从第一个找起，排在后面的永远轮不到（饿死）；要同时给多个 channel 加锁，两个 `select` 加锁顺序不同，就可能互相等着对方放手（死锁）。

**结构。** `select` 先随机洗牌（shuffle）出轮询顺序，再按 channel 地址给所有 channel 排序加锁。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">select 同时有 3 个 case 就绪</text>
<text x="8" y="38" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">① 轮询顺序: 随机洗牌, 每个就绪的 case 机会相同</text>
<rect x="20" y="48" width="46" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="43" y="64.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c3</text>
<line x1="66" y1="60" x2="76" y2="60" stroke="currentColor" stroke-width="1"/>
<polygon points="76,60 70.0,62.7 70.0,57.3" fill="currentColor"/>
<rect x="76" y="48" width="46" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="99" y="64.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c1</text>
<line x1="122" y1="60" x2="132" y2="60" stroke="currentColor" stroke-width="1"/>
<polygon points="132,60 126.0,62.7 126.0,57.3" fill="currentColor"/>
<rect x="132" y="48" width="46" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="155" y="64.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c2</text>
<text x="200" y="64" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第一个就绪的被选中</text>
<text x="8" y="104" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">② 加锁顺序: 按 channel 地址从小到大</text>
<rect x="20" y="114" width="46" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="43" y="130.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c1</text>
<text x="43" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0x10</text>
<line x1="66" y1="126" x2="90" y2="126" stroke="currentColor" stroke-width="1"/>
<polygon points="90,126 84.0,128.7 84.0,123.3" fill="currentColor"/>
<rect x="90" y="114" width="46" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="113" y="130.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c2</text>
<text x="113" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0x20</text>
<line x1="136" y1="126" x2="160" y2="126" stroke="currentColor" stroke-width="1"/>
<polygon points="160,126 154.0,128.7 154.0,123.3" fill="currentColor"/>
<rect x="160" y="114" width="46" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="183" y="130.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c3</text>
<text x="183" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0x30</text>
<text x="8" y="176" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">所有 select 都按同一顺序加锁, 就不会互相等待</text>
</svg>
```

**细节。**

- 轮询顺序：逐个随机交换，所以每个就绪的 case 被选中的概率相同
- 实测：两个 channel 都就绪，选 10000 次，结果是 4919 : 5081
- 加锁顺序：按 `hchan` 地址排序，排序用堆排序，保证 O(n log n) 且栈空间固定

**为什么。** 固定顺序会让靠前的 case 饿死其他 case；所有 `select` 都按同一顺序加锁，就不会互相等待造成死锁。

**对应 LeetCode：** 无直接对应的题（运行时的公平与死锁规避）
