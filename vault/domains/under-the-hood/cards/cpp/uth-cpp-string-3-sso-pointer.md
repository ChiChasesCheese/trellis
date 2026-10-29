---
id: uth-cpp-string-3-sso-pointer
node: cpp.string
type: qa
step: 3
---
## Q
**string 移动后 data() 指针为什么变了**｜C++ · std::string

`vector<string>` 扩容后，之前存下的 `const char*` 有时还能用，有时就悬空，为什么？

## A
**背景。** `vector` 扩容要把每个 `string` 对象搬进新内存块。移动（move）就是把内容交给新对象、不重新拷贝全部字符。长字符串的对象里只有一个指向堆的指针，换个主人即可；短字符串的字符就住在对象里面。

**结构。** 短字符串存在 `string` 对象内部，`data()` 指向对象自己；长字符串在堆上。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">vector&lt;string&gt; 扩容: 对象被搬到新块</text>
<rect x="10" y="24" width="132" height="60" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="16" y="30" width="58" height="48" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="45" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">短串</text>
<text x="45" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内联 hi</text>
<rect x="78" y="30" width="58" height="48" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="107" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">长串</text>
<text x="107" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ptr</text>
<rect x="190" y="24" width="132" height="60" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="196" y="30" width="58" height="48" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="225" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">短串</text>
<text x="225" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内联 hi</text>
<rect x="258" y="30" width="58" height="48" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="287" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">长串</text>
<text x="287" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ptr</text>
<line x1="142" y1="54" x2="190" y2="54" stroke="currentColor" stroke-width="1"/>
<polygon points="190,54 184.0,56.7 184.0,51.3" fill="currentColor"/>
<text x="166" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">搬</text>
<rect x="60" y="140" width="240" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="180" y="158.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆上的长字符 (地址不动)</text>
<line x1="107" y1="78" x2="107" y2="140" stroke="currentColor" stroke-width="1"/>
<polygon points="107,140 104.3,134.0 109.7,134.0" fill="currentColor"/>
<line x1="287" y1="78" x2="287" y2="140" stroke="currentColor" stroke-width="1"/>
<polygon points="287,140 284.3,134.0 289.7,134.0" fill="currentColor"/>
<rect x="14" y="104" width="50" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="39" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<line x1="39" y1="104" x2="39" y2="80" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="39,80 41.7,86.0 36.3,86.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="72" y="120" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">悬空</text>
<text x="8" y="190" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">p1 指着旧块里的内联字符: 搬走就悬空</text>
<text x="8" y="204" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长串的字符还在原处, 指针仍有效</text>
</svg>
```

**细节。**

- 扩容时 `string` 被移动：堆上的字符只是指针换主人，地址不变
- 内联的字符必须逐字节拷到新对象里，地址跟着变
- libc++ 实测：长度 5 的字符串扩容后 `data()` 变了，长度 40 的没变

**为什么。** 内联存储省了一次分配，代价是失去地址稳定。

**坑。** 长字符串“碰巧没问题”，短字符串一用就崩；`string_view`（只看不拥有的字符视图）同理。

**对应 LeetCode：** 无直接对应的题（内存地址的稳定性）
