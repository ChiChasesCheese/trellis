---
id: uth-cpp-string-2-cow
node: cpp.string
type: qa
step: 2
---
## Q
**写时复制字符串为什么被 C++11 禁止**｜C++ · libstdc++ 的 std::string

老版 GCC 的 `std::string` 拷贝时共享缓冲、引用计数加一。C++11 为什么不让这样实现了？

## A
**背景。** 拷贝字符串很贵：要把所有字符再复制一份。老版 GCC 想偷懒：两个字符串先共用同一块缓冲，只记一个引用计数（有几个字符串在用它）；谁要修改，才复制一份给谁。

**结构。** 写时复制（Copy-On-Write，COW）：拷贝只共享缓冲，谁先修改谁再复制一份。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">COW:拷贝只加引用计数</text>
<rect x="10" y="24" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="30" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">s1</text>
<rect x="10" y="62" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="30" y="78.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">s2</text>
<rect x="150" y="36" width="110" height="38" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="205" y="59.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">rc=2  abc</text>
<line x1="50" y1="36" x2="150" y2="48" stroke="currentColor" stroke-width="1"/>
<polygon points="150,48 143.7,50.0 144.4,44.6" fill="currentColor"/>
<line x1="50" y1="74" x2="150" y2="64" stroke="currentColor" stroke-width="1"/>
<polygon points="150,64 144.3,67.3 143.8,61.9" fill="currentColor"/>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">s1[0] = 'x' 之前,先给 s1 复制私有缓冲</text>
<rect x="10" y="124" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="30" y="140.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">s1</text>
<rect x="150" y="124" width="110" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="205" y="140.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xbc</text>
<line x1="50" y1="136" x2="150" y2="136" stroke="currentColor" stroke-width="1"/>
<polygon points="150,136 144.0,138.7 144.0,133.3" fill="currentColor"/>
<rect x="10" y="156" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="30" y="172.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">r</text>
<line x1="50" y1="168" x2="150" y2="168" style="stroke:var(--accent,#3b6fd4)" stroke-width="1" stroke-dasharray="4 3"/>
<text x="300" y="172" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">悬空</text>
<rect x="150" y="156" width="110" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="205" y="172.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧缓冲 abc</text>
</svg>
```

**细节。**

- C++11 规定非 const 的 `operator[]`、`begin()` 等不能使已经拿到的引用、指针、迭代器失效
- COW 下，非 const 的 `operator[]` 得先把共享缓冲复制成私有的，旧引用立刻悬空（指向已经不用的内存）
- GCC 5.1 起 libstdc++ 引入新 ABI 取消 COW，宏 `_GLIBCXX_USE_CXX11_ABI` 控制用哪个

**为什么。** “修改时才复制”与“引用仍然有效”互相冲突，于是每个字符串独占缓冲，再靠 SSO 压低拷贝成本。

**对应 LeetCode：** 无直接对应的题（内存与拷贝的取舍）
