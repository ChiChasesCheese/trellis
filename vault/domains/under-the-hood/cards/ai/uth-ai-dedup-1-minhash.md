---
id: uth-ai-dedup-1-minhash
node: ai.dedup
type: qa
step: 1
---
## Q
**两篇文章像不像，不比全文**｜datatrove · 0.8.0 MinHash

几十亿篇网页里有大量转载和模板拼接，怎么不逐字比较，就估出两篇有多像？

## A
**背景。** 训练前要去掉重复文章，否则模型会背下来。n 篇两两比较要 n² 次，几十亿篇做不到。先把「像」量化：每篇切成连续 5 个词的小片段（shingle，datatrove 默认 `n_grams = 5`），相似度 = 共有片段数 ÷ 合起来的片段数（Jaccard 相似度）。可每次比较仍要读整篇。

**结构。** 最小哈希（MinHash）：给所有片段随机排一次队，每篇文章只记「自己的片段里排最前的那个」。换一种排法再记一个，共记 112 次，一篇文章就压成 112 个数的签名。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 258">
<g font-size="12" font-family="sans-serif" text-anchor="middle" fill="currentColor" stroke="currentColor">
<text x="100" y="18" font-size="13" font-weight="bold" stroke="none">A=abcd</text>
<text x="250" y="18" font-size="13" font-weight="bold" stroke="none">B=bcde</text>
<text x="170" y="36" style="stroke:none;fill:var(--dim,#6b7280)">共有3个, 合起来5个: 相似度3/5</text>
<text x="10" y="62" text-anchor="start" style="stroke:none;fill:var(--dim,#6b7280)">排列顺序</text>
<text x="150" y="62" text-anchor="start" style="stroke:none;fill:var(--dim,#6b7280)">A的第一个</text>
<text x="225" y="62" text-anchor="start" style="stroke:none;fill:var(--dim,#6b7280)">B的第一个</text>
<text x="305" y="62" text-anchor="start" style="stroke:none;fill:var(--dim,#6b7280)">相同</text>
<rect x="4" y="74" width="332" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:none"/>
<text x="10" y="90" text-anchor="start" stroke="none">caedb</text>
<text x="170" y="90" stroke="none">c</text>
<text x="245" y="90" stroke="none">c</text>
<text x="318" y="90" style="stroke:none;fill:var(--accent,#3b6fd4)">是</text>
<text x="10" y="116" text-anchor="start" stroke="none">ebacd</text>
<text x="170" y="116" stroke="none">b</text>
<text x="245" y="116" stroke="none">e</text>
<text x="318" y="116" style="stroke:none;fill:var(--dim,#6b7280)">否</text>
<text x="10" y="142" text-anchor="start" stroke="none">adcbe</text>
<text x="170" y="142" stroke="none">a</text>
<text x="245" y="142" stroke="none">d</text>
<text x="318" y="142" style="stroke:none;fill:var(--dim,#6b7280)">否</text>
<rect x="4" y="152" width="332" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:none"/>
<text x="10" y="168" text-anchor="start" stroke="none">dcbae</text>
<text x="170" y="168" stroke="none">d</text>
<text x="245" y="168" stroke="none">d</text>
<text x="318" y="168" style="stroke:none;fill:var(--accent,#3b6fd4)">是</text>
<rect x="4" y="178" width="332" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:none"/>
<text x="10" y="194" text-anchor="start" stroke="none">bedac</text>
<text x="170" y="194" stroke="none">b</text>
<text x="245" y="194" stroke="none">b</text>
<text x="318" y="194" style="stroke:none;fill:var(--accent,#3b6fd4)">是</text>
<line x1="4" y1="224" x2="336" y2="224" style="stroke-width:1"/>
<text x="170" y="246" font-size="13" font-weight="bold" stroke="none">5次里相同3次 = 0.6 = 相似度</text>
</g>
</svg>
```

**细节。**

- 为什么相同次数就是相似度：合起来的 5 个片段里排第一的那个，只有落在共有的 3 个里，两篇的「第一」才相同，概率正是 3/5
- 实现里不真排队，用 `(a·x + b) mod p` 这类随机函数代替，`p = 2^61 − 1`
- 默认 14 段 × 每段 8 个 = 112 个哈希

**为什么。** 签名长度固定：文章多长都是 112 个数，比较两篇只看签名。

**对应 LeetCode：** 无直接对应的题
