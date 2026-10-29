---
id: uth-devtools-diff-2-preprocess
node: devtools.diff
type: qa
step: 2
---
## Q
**diff 先做了哪些预处理**｜Git · xdiff · 2.56

真正跑 Myers 之前，git 怎么先把问题变小？

## A
**背景。** 典型的改动只占文件很小一段，开头和结尾成千上万行完全相同；把这些行也喂给核心算法是浪费。所以 git 在跑 Myers 之前，先把问题变小。

**结构。** 先把每一行映射成一个整数，之后比较两行只是比较两个整数；再剪头去尾，并丢掉“注定对不上”的行，核心算法只面对剩下的一小段。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="120" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">旧</text>
<text x="220" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">新</text>
<rect x="100" y="34" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="120" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="100" y="62" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="120" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<rect x="100" y="90" width="40" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="120" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<rect x="100" y="118" width="40" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="120" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<rect x="100" y="146" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="120" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<rect x="100" y="174" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="120" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">6</text>
<rect x="200" y="34" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="220" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="200" y="62" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="220" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<rect x="200" y="90" width="40" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="220" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">7</text>
<rect x="200" y="118" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="220" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<rect x="200" y="146" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="220" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">6</text>
<line x1="140" y1="45" x2="200" y2="45" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="140" y1="73" x2="200" y2="73" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="140" y1="157" x2="200" y2="129" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="140" y1="185" x2="200" y2="157" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="250" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">头部相同 剪掉</text>
<text x="250" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">只比这里</text>
<text x="250" y="158" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">尾部相同 剪掉</text>
<text x="10" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">另一边没有</text>
<text x="10" y="122" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">直接判删</text>
<text x="170" y="236" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每行先映射成一个整数 再比较整数</text>
</svg>
```

**细节。**

- 先剪掉开头和结尾完全相同的行
- 在另一个文件里根本没出现的行，直接判为增或删，不进入主算法
- 在另一文件里出现次数过多的行（上限约为行数的平方根，最多 1024），夹在可丢弃的行中间时也会被丢弃

**为什么。** 典型的改动只占文件一小段，剪掉两头和“注定不匹配”的行，核心算法面对的就小得多。

**坑。** 丢弃高频行是启发式，结果可能不是最短；`--minimal` 会把这个上限取消。

**对应 LeetCode：** 无直接对应的题
