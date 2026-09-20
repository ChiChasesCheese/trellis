---
nodes: [problems.components.text-editor]
url: https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation
---
# Text Buffer Reimplementation（VS Code 工程博客）

值得读：工程上把"编辑器的正文该用什么数据结构"讲得最透的一篇。VS Code 原来用按行的字符串数组，
打开大文件时内存和启动延迟都受不了，于是换成 **piece table**，再把片段列表换成平衡树（piece
tree）以便按行号和偏移都能 O(log n) 定位；文中给了真实的内存占用与操作延迟对比，还讲了换行符
处理这类"理论文章不会提、真实实现躲不掉"的细节。本题解选 gap buffer 而不是 piece table，
理由和它的取舍正好互补：piece table 最大的红利是"快照近乎免费"，而这里的撤销已经用增量
（`Edit`）实现，不需要便宜的快照；反过来，一旦要支持多光标或超大文件，本题解也会倒向它的选择。
