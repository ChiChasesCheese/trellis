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
**结构。** 片段表（piece table）：原文件缓冲区加一个只追加的新增缓冲区，文档是一串“片段”（缓冲区，起点，长度）。VS Code 把片段放进红黑树，叫 piece tree。

**细节。**

- 旧实现每行一个对象：35 MB 的文件占约 600 MB，约 20 倍
- piece tree 刚加载完，内存接近文件本身的大小
- 每个节点缓存左子树的字符数和换行数，按行号查找是 O(log N)
- 编辑只增删片段，不拷贝原文

**为什么。** 内存与文件大小同阶，编辑只改片段表，不动大块文本。

**对应 LeetCode：** LC 307 区域和检索 - 数组可修改 · LC 2296 设计一个文本编辑器
