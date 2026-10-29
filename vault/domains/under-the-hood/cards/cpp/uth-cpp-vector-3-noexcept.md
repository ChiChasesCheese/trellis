---
id: uth-cpp-vector-3-noexcept
node: cpp.vector
type: qa
step: 3
---
## Q
**扩容是搬还是拷**｜C++ · std::vector

自定义类型放进 `vector`，扩容时元素是被移动（move）还是被拷贝（copy）？

## A
**背景。** 扩容要把旧元素“搬”到新块，有两种搬法：拷贝（copy）原样复制一份，旧的完好；移动（move）把内容交给新对象，旧的被掏空，通常更快。但搬到一半如果抛出异常，被掏空的旧块没法恢复。

**结构。** 扩容时逐个把旧块元素构造到新块里，用的是 `move_if_noexcept`：只有确认移动不会抛异常才用移动。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="100" y="10" width="140" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="170" y="28.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扩容:搬每个元素</text>
<line x1="170" y1="38" x2="170" y2="56" stroke="currentColor" stroke-width="1"/>
<polygon points="170,56 167.3,50.0 172.7,50.0" fill="currentColor"/>
<rect x="80" y="56" width="180" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="170" y="75.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">移动构造 noexcept ?</text>
<line x1="110" y1="86" x2="70" y2="116" stroke="currentColor" stroke-width="1"/>
<polygon points="70,116 73.2,110.2 76.4,114.6" fill="currentColor"/>
<text x="70" y="106" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<rect x="10" y="116" width="120" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="70" y="134.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">移动 move</text>
<text x="70" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧块被掏空也没事</text>
<line x1="230" y1="86" x2="270" y2="116" stroke="currentColor" stroke-width="1"/>
<polygon points="270,116 263.6,114.6 266.8,110.2" fill="currentColor"/>
<text x="270" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">否</text>
<rect x="200" y="116" width="130" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="265" y="134.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有拷贝构造?拷贝</text>
<text x="265" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧块完好,可回滚</text>
<text x="170" y="192" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">move_if_noexcept:怕搬到一半抛异常</text>
</svg>
```

**细节。**

- 移动构造声明了 `noexcept`（承诺不抛异常）：移动
- 没声明但有拷贝构造：退回拷贝
- libc++ 实测：同样的类，加上 `noexcept` 后扩容打印从 copy 变成 move

**为什么。** 拷贝则旧块完好，扩容要么全成功要么什么都没变（强异常保证）。

**坑。** 自定义类型漏写 `noexcept`，`vector` 扩容就悄悄变成逐个深拷贝。

**对应 LeetCode：** 无直接对应的题（异常安全的取舍）
