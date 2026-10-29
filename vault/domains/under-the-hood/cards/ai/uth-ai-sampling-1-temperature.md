---
id: uth-ai-sampling-1-temperature
node: ai.sampling
type: qa
step: 1
---
## Q
**模型怎样选出下一个字**｜transformers · 5.21

语言模型每一步给词表里每个词打一个分，下一个词是怎样从分数里选出来的？温度（temperature）调的是什么？

## A
**背景。** 模型每步输出一串分数（logits），词表有多少词就有多少个分。最省事的办法是永远选最高分（贪心，greedy）：但每次答案都一样，还容易车轱辘话重复。想要变化，就按概率抽签：先把分数变成概率，再抽。

**结构。** softmax：每个分数先取指数 `e^x`，再除以总和，得到加起来为 1 的概率。温度 `T` 只多做一步：softmax 之前，先把所有分数除以 `T`（源码就是 `scores / temperature`）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="84" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">温度 1</text>
<rect x="18" y="75.6" width="26" height="64.4" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="31" y="70.6" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">64%</text>
<text x="31" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">好</text>
<rect x="52" y="116.3" width="26" height="23.7" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="65" y="111.3" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">24%</text>
<text x="65" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">热</text>
<rect x="86" y="131.3" width="26" height="8.7" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="99" y="126.3" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">9%</text>
<text x="99" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冷</text>
<rect x="120" y="136.8" width="26" height="3.2" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="133" y="131.8" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3%</text>
<text x="133" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">差</text>
<text x="252" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">温度 0.5</text>
<rect x="186" y="53.5" width="26" height="86.5" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="199" y="48.5" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">86%</text>
<text x="199" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">好</text>
<rect x="220" y="128.3" width="26" height="11.7" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="233" y="123.3" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">12%</text>
<text x="233" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">热</text>
<rect x="254" y="138" width="26" height="2" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="267" y="133" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2%</text>
<text x="267" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冷</text>
<rect x="288" y="138" width="26" height="2" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="301" y="133" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0.2%</text>
<text x="301" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">差</text>
<line x1="10" y1="140" x2="330" y2="140" stroke="currentColor" stroke-width="1"/>
<text x="170" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分数相同, 只改温度, 分布变尖或变平</text>
</svg>
```

**细节。**

- 例：「今天天气很」之后，分数 2、1、0、-1 对应 好、热、冷、差
- `T=1`：64% / 24% / 9% / 3%；`T=0.5`：86% / 12% / 2% / 0.2%；`T=2`：46% / 28% / 17% / 10%
- transformers 要求 `T` 严格大于 0；想要贪心就关掉采样（`do_sample=False`），不是设 `T=0`

**为什么。** 除以 `T` 不改变词的名次，只改变分布的尖和平：`T` 小，头部更突出；`T` 大，机会更均匀。

**对应 LeetCode：** 无直接对应的题
