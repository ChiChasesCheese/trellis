---
id: uth-cpp-string-1-sso
node: cpp.string
type: qa
step: 1
---
## Q
**短字符串为什么不分配堆内存**｜C++ · libstdc++ 16 / libc++ 23

`std::string s = "hello"` 要不要 `malloc`？多长的字符串才会走到堆上？

## A
**背景。** 字符放在堆上（程序运行时向系统另要的内存），每次创建要 `malloc`（向系统要内存）、销毁要 `free`，读字符还要多跳一次指针。可现实里的字符串大多很短，`"hello"` 才 5 个字节，比一个 8 字节的指针还小。

**结构。** 小字符串优化（Small String Optimization，SSO）：对象里留一小段缓冲，字符串够短就直接存在里面，否则存堆指针。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">短串: 字符就在对象里 (libstdc++ 32 字节)</text>
<rect x="10" y="26" width="54" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="37" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ptr</text>
<rect x="64" y="26" width="54" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="91" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">size 5</text>
<rect x="118" y="26" width="190" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="213" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h e l l o \0 ... 共 16 字节</text>
<path d="M37 52 L37 62 L140 62 L140 54" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="140,52 142.7,58.0 137.3,58.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="150" y="76" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ptr 指回自己的缓冲</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">长串: ptr 指向堆, 联合体里记容量</text>
<rect x="10" y="116" width="54" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="37" y="133.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ptr</text>
<rect x="64" y="116" width="54" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="91" y="133.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">size 40</text>
<rect x="118" y="116" width="190" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="213" y="133.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">capacity</text>
<line x1="37" y1="142" x2="37" y2="160" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="37,160 34.3,154.0 39.7,154.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="160" width="298" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="159" y="177.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆上的 40+ 字节 (一次 malloc)</text>
<text x="8" y="202" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">libc++: 对象 24 字节, 内联 22 字符</text>
</svg>
```

**细节。**

- libstdc++：对象 32 字节（指针、长度、一个 16 字节的联合体，同一块内存两种用法：短时放字符，长时放容量），最多内联 15 个字符
- libc++：对象 24 字节，最多内联 22 个字符
- libc++ 实测：22 个字符的 `data()` 指向对象内部，23 个就跑到堆上

**为什么。** 实际程序里绝大多数字符串很短（标识符、键名、路径片段），省掉一次 `malloc`/`free` 和一次指针跳转，缓存也更友好。

**对应 LeetCode：** 无直接对应的题（内存布局的优化）
