---
id: uth-java-string-1-compact
node: java.string
type: qa
step: 1
---
## Q
**Java 字符串一个字符占几个字节**｜Java · OpenJDK 25（Java 9 起）

`"hello"` 和 `"你好世界"` 在 `String` 内部各占多少字节？只混进一个非拉丁字符会怎样？

## A
**背景。** Java 8 及以前，`String` 用 `char[]`，每个字符固定 2 字节。可程序里的字符串绝大多数只有英文字母，一半空间白白浪费。

**结构。** Java 9 起，`String` 内部是 `byte[] value` 加一个标志 `coder`：`LATIN1`（每字符 1 字节）或 `UTF16`（每字符 2 字节），整串统一。字符都在 Latin-1 范围内就用 1 字节，混进一个超出范围的字符，整串都改成 2 字节。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="20" y="24" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hello  coder = LATIN1</text>
<rect x="26" y="34" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="38" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h</text>
<rect x="50" y="34" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="62" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="74" y="34" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="86" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<rect x="98" y="34" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="110" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<rect x="122" y="34" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="134" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<text x="160" y="52" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5 字节</text>
<text x="20" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hello€  coder = UTF16</text>
<rect x="26" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="38" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h</text>
<rect x="50" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="74" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="86" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="98" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="122" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="134" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<rect x="146" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="170" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="182" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<rect x="194" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="218" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="230" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<rect x="242" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="266" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="278" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">€</text>
<rect x="290" y="116" width="24" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6 个字符 12 字节 一个 € 让整串变宽</text>
</svg>
```

**细节。**

- 实测：`"hello world"` 11 个字符占 11 字节，`"héllo"` 5 字节（Latin-1 够用）。
- `"你好世界"` 4 个字符占 8 字节；`"hello€"` 6 个字符占 12 字节：一个 `€` 就让整串变成 UTF-16。

**为什么。** 实际程序里大多数字符串是 Latin-1，字节数组省下约一半内存和缓存；代价是每次取字符要先看 `coder`。

**对应 LeetCode：** 无直接对应的题
