---
id: uth-python-str-int-1-str-kinds
node: python.str-int
type: qa
step: 1
---
## Q
**str 每个字符占几个字节**｜Python · CPython 3.14

为什么 10 个 ASCII 字符的字符串占 51 字节，10 个汉字占 78 字节，10 个 emoji 占 100 字节？

## A
**背景。** 想让 `s[i]` 秒取，最好每个字符一样宽：第 i 个就在起点 + i × 宽度。可字符的大小不一，英文字母 1 字节就够，emoji 要 4 字节。UTF-8 为了省空间让字符变长，取第 i 个就得从头数。

**结构。** CPython 的办法（PEP 393）：一个字符串里所有字符共用同一种宽度，按最宽的那个字符选 1、2 或 4 字节。全是英文就 1 字节，混进一个 emoji，整串都变成每字符 4 字节。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="10" y="48" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ASCII</text>
<rect x="64" y="30" width="22" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="75" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1B</text>
<rect x="86" y="30" width="22" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="97" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1B</text>
<rect x="108" y="30" width="22" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="119" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1B</text>
<text x="10" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">汉字</text>
<rect x="64" y="76" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="86" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2B</text>
<rect x="108" y="76" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2B</text>
<rect x="152" y="76" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="174" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2B</text>
<text x="10" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">表情</text>
<rect x="64" y="122" width="88" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="108" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4B</text>
<rect x="152" y="122" width="88" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="196" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4B</text>
<rect x="240" y="122" width="88" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="284" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4B</text>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">整串按最宽的字符统一宽度 s[i] 一步取到</text>
</svg>
```

**细节。**

- 实测 `getsizeof`：`'a'*10` 为 51，`'é'*10` 为 67，`'中'*10` 为 78，`'😀'*10` 为 100。
- 纯 ASCII 的对象头更小（40 字节），其余是 56 字节；另加结尾的空字符。

**为什么。** 固定宽度换来 O(1) 下标，代价是一个 emoji 会让整串膨胀到 4 倍。

**对应 LeetCode：** 无直接对应的题
