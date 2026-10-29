---
id: uth-ai-tokenizer-2-pretokenize
node: ai.tokenizer
type: qa
step: 2
---
## Q
**编码前先用正则切词**｜tiktoken 0.14 · cl100k_base

为什么 tiktoken 先用一条正则把文本切开，再逐段合并？同一个词前面有没有空格，编号为什么不一样？

## A
**背景。** 如果对整段文本直接合并，`dog.`、`dog!`、`dog?` 会各自粘出带标点的怪块，白占词表；数字、换行也会和字母粘在一起。办法：合并之前先用正则表达式（regular expression，按模式切字符串的规则）把文本切成一段段「词」，合并只在词内部进行。

**结构。** 编码分两步：正则切词，再对每个词单独做 BPE。空格归后面的词，所以 `strawberry` 和带前导空格的 `_strawberry`（`_` 表示空格）是两个不同的词，各有各的切法。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="12" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">strawberry: 3 个编号</text>
<rect x="12" y="24" width="40" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="32" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">str</text>
<rect x="56" y="24" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="72" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">aw</text>
<rect x="92" y="24" width="56" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="120" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">berry</text>
<text x="12" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">_strawberry (前面带空格): 1 个编号</text>
<rect x="12" y="84" width="110" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="67" y="101.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">_strawberry</text>
<text x="12" y="136" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12345678: 数字最多 3 位一组</text>
<rect x="12" y="144" width="44" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="34" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">123</text>
<rect x="60" y="144" width="44" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="82" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">456</text>
<rect x="108" y="144" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="126" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">78</text>
<text x="170" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">_ 表示空格; 空格归后面的词</text>
</svg>
```

**细节。**

- 实测 cl100k_base：`strawberry` 切成 `str`+`aw`+`berry`，`_strawberry` 只要 1 个编号
- 数字最多 3 位一组（正则里的 `\p{N}{1,3}`）
- 词表里放的是字节：`日本語` 共 9 字节，变成 4 个编号，最后一个字被劈成两半

**坑。** 编号数不等于字符数：`😀` 就占 2 个编号。估算费用和上下文长度要用分词器真数，别用字符数。

**对应 LeetCode：** 无直接对应的题
