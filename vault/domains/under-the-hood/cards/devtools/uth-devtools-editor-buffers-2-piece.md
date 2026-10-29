---
id: uth-devtools-editor-buffers-2-piece
node: devtools.editor-buffers
type: qa
step: 2
---
## Q
**VS Code 的 piece tree**｜VS Code · 1.21 起

打开 35 MB、1370 万行的文件，旧的“每行一个字符串”为什么要吃约 600 MB？

## A
**背景。** 打开一个 35 MB、1370 万行的文件，旧的“每行一个字符串对象”要吃约 600 MB。另一条路是根本不拷贝文本：原文件放着不动，新打的字追加到另一块缓冲区，文档只是一张“片段表”，每个片段说“取哪块缓冲区、从哪开始、多长”。

**结构。** 片段表（piece table）：原文件缓冲区加一个只追加的新增缓冲区，文档是一串片段。VS Code 把片段放进红黑树，叫 piece tree。例：原文 `the quick fox`，在第 10 个字符后插入 `brown `：文档 = 原文前 10 个字符 + 新增缓冲区的 `brown ` + 原文剩下的 3 个字符，原文一个字节都没动。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<text x="20" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">原文缓冲区 不再改动</text>
<rect x="20" y="22" width="182" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="111" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">the quick fox</text>
<text x="20" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">新增缓冲区 只追加</text>
<rect x="20" y="76" width="84" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="62" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">brown</text>
<text x="20" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">文档 = 三个片段连起来</text>
<rect x="20" y="130" width="140" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">the quick</text>
<rect x="160" y="130" width="84" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="202" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">brown</text>
<rect x="244" y="130" width="42" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">fox</text>
<text x="20" y="182" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">片段 1  原文 从 0 起 长 10</text>
<text x="20" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">片段 2  新增 从 0 起 长 6</text>
<text x="20" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">片段 3  原文 从 10 起 长 3</text>
</svg>
```

**细节。**

- 旧实现每行一个对象：35 MB 的文件占约 600 MB，约 20 倍；piece tree 刚加载完，内存接近文件本身的大小
- 每个节点缓存左子树的字符数和换行数，按行号查找是 O(log N)
- 编辑只增删片段，不拷贝原文

**为什么。** 内存与文件大小同阶，编辑只改片段表，不动大块文本。

**对应 LeetCode：** 无直接对应的题
