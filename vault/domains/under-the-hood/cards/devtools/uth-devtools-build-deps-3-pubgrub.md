---
id: uth-devtools-build-deps-3-pubgrub
node: devtools.build-deps
type: qa
step: 3
---
## Q
**uv 的回溯聪明在哪**｜uv · PubGrub

同样是版本回溯，uv 为什么更快，失败时的报错也更好懂？

## A
**背景。** 朴素回溯有个浪费：同一个矛盾可能在搜索的不同角落反复撞上，每次都重新试一遍。PubGrub 算法每撞上一次冲突，就把原因总结成一条通用结论（不兼容集，incompatibility）记下来；以后凡是违反它的选择，不必再试。uv 用的就是 PubGrub。

**结构。** 例：`a 2` 需要 `c 1`，`b 2` 需要 `c 2`，而 c 只能选一个版本，就记下“`a 2` 和 `b 2` 不能同时选”。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="34" y="37" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a 2</text>
<rect x="34" y="117" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b 2</text>
<rect x="234" y="37" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c 1</text>
<rect x="234" y="117" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c 2</text>
<line x1="88" y1="50" x2="225" y2="50" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M230.0,50.0 L223.2,53.3 L223.2,46.7 Z" fill="currentColor" stroke="none"/>
<line x1="88" y1="130" x2="225" y2="130" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M230.0,130.0 L223.2,133.3 L223.2,126.7 Z" fill="currentColor" stroke="none"/>
<text x="160" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">需要</text>
<text x="160" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">需要</text>
<line x1="260" y1="66" x2="260" y2="112" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="270" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">只能选一个</text>
<rect x="26" y="28" width="68" height="124" rx="3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">记下 a 2 和 b 2 不能同时选</text>
</svg>
```

**细节。**

- 无解时，这些不兼容集可以还原成指出具体包的错误信息，而不是一句“无解”
- uv 的版本从高到低尝试，优先沿用锁文件（记录上次解析结果的文件）里的版本
- 官方文档说最慢的一步是读取元数据，不是算法

**为什么。** 重复失败的组合被一次性排除；现实中的依赖是连续的版本区间，多数解析根本不需要回溯。

**对应 LeetCode：** 无直接对应的题
