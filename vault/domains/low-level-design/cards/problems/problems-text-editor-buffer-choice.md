---
id: problems-text-editor-buffer-choice
node: problems.components.text-editor
type: qa
step: 1
tags: [grown]
---
## Q
设计一个能打开几 MB 源文件的文本编辑器，正文该用一个 Python `str`、一个按行的 `list[str]`、一个 gap buffer（空洞缓冲），还是一个 piece table（片段表）？

## A
先看关键操作的代价：一个 `str` 每次插入都是 `text[:i] + s + text[i:]`，**整篇复制 O(n)**——10 MB 的文档每敲一个字符复制 10 MB，直接出局；按行的列表在行内是 O(行长)、增删行是 O(行数)，对多数编辑器够用，但一行特别长时退化；gap buffer 把空洞停在光标处，连续插入删除是**摊销 O(1)**，代价是移动光标要搬运 O(距离) 的字符；piece table 原文永不复制、可以 mmap 大文件、快照近乎免费，但实现复杂一个量级。

面试里选 gap buffer 通常最划算：它押注的"编辑是局部的"正是真实的打字行为，八十行就能写对。选 piece table 的唯一强理由是需要廉价快照或超大文件——如果撤销已经用增量实现，这个红利就用不上了。
